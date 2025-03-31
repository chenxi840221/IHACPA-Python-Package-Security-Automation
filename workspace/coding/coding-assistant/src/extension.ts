// src/extension.ts

import * as vscode from 'vscode';
import { ClaudeService } from './services/claudeService';


// This class implements the TreeDataProvider interface
class CodingAssistantProvider implements vscode.TreeDataProvider<AssistantItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<AssistantItem | undefined | null | void> = new vscode.EventEmitter<AssistantItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<AssistantItem | undefined | null | void> = this._onDidChangeTreeData.event;
  
    refresh(): void {
      this._onDidChangeTreeData.fire();
    }
  
    getTreeItem(element: AssistantItem): vscode.TreeItem {
      return element;
    }
  
    getChildren(element?: AssistantItem): Thenable<AssistantItem[]> {
      if (element) {
        return Promise.resolve([]);
      } else {
        // Return top-level items
        return Promise.resolve([
          new AssistantItem('Get Help', 'Get coding assistance', vscode.TreeItemCollapsibleState.None, {
            command: 'codingAssistant.getHelp',
            title: 'Get Help',
            arguments: []
          }),
          new AssistantItem('Explain Code', 'Explain selected code', vscode.TreeItemCollapsibleState.None, {
            command: 'codingAssistant.explainCode',
            title: 'Explain Code',
            arguments: []
          })
        ]);
        }
    }
}
  
  // Tree item class
  class AssistantItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        descriptionText: string, // Changed from 'private description' to 'descriptionText'
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly command?: vscode.Command
    ) {
        super(label, collapsibleState);
        this.tooltip = descriptionText;
        this.description = descriptionText; // Now this uses the inherited description property
    }
}

export function activate(context: vscode.ExtensionContext) {
    console.log('Coding Assistant is now active!');

    const codingAssistantProvider = new CodingAssistantProvider();
    vscode.window.registerTreeDataProvider('codingAssistantPanel', codingAssistantProvider);
    
    // Optionally add a command to refresh the view
    context.subscriptions.push(
      vscode.commands.registerCommand('codingAssistant.refreshView', () => {
        codingAssistantProvider.refresh();
      })
    );

    // Create instance of Claude service
    const claudeService = new ClaudeService();
    
    // Register command to get coding help
    let getHelpCommand = vscode.commands.registerCommand('codingAssistant.getHelp', async () => {
        const editor = vscode.window.activeTextEditor;
        
        if (!editor) {
            vscode.window.showInformationMessage('No active editor found');
            return;
        }
        
        // Check if API key is configured
        if (!claudeService.isConfigured()) {
            const setKey = 'Set API Key';
            const response = await vscode.window.showErrorMessage(
                'Anthropic API key not configured. Please set your API key in the extension settings.',
                setKey
            );
            
            if (response === setKey) {
                vscode.commands.executeCommand('workbench.action.openSettings', 'codingAssistant.apiKey');
            }
            return;
        }

        // Get selected text or current line
        const selection = editor.selection;
        const text = selection.isEmpty 
            ? editor.document.lineAt(selection.active.line).text
            : editor.document.getText(selection);
        
        // Get document language
        const language = editor.document.languageId;
        
        // Show input box for user query
        const userQuery = await vscode.window.showInputBox({
            placeHolder: 'What do you need help with?',
            prompt: 'Enter your coding question',
            value: `Help with: ${text.length > 30 ? text.substring(0, 30) + '...' : text}`
        });

        if (!userQuery) return;

        // Show progress indicator
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "Getting coding assistance...",
            cancellable: false
        }, async (progress) => {
            progress.report({ increment: 0 });
            
            try {
                // Call Claude API
                const response = await claudeService.getCodingAssistance(userQuery, text, language);
                progress.report({ increment: 100 });
                
                if (response.error) {
                    vscode.window.showErrorMessage(`Error: ${response.error}`);
                    return;
                }
                
                // Show response in webview panel
                showResponsePanel(userQuery, response.content, language);
            } catch (error) {
                vscode.window.showErrorMessage(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
            }
        });
    });
    
    // Register command to explain code
    let explainCodeCommand = vscode.commands.registerTextEditorCommand('codingAssistant.explainCode', async (textEditor) => {
        // Check if API key is configured
        if (!claudeService.isConfigured()) {
            const setKey = 'Set API Key';
            const response = await vscode.window.showErrorMessage(
                'Anthropic API key not configured. Please set your API key in the extension settings.',
                setKey
            );
            
            if (response === setKey) {
                vscode.commands.executeCommand('workbench.action.openSettings', 'codingAssistant.apiKey');
            }
            return;
        }

        const selection = textEditor.selection;
        const selectedText = textEditor.document.getText(selection);
        
        if (!selectedText) {
            vscode.window.showInformationMessage('Please select some code to explain');
            return;
        }
        
        // Get document language
        const language = textEditor.document.languageId;
        
        // Show progress indicator
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "Analyzing code...",
            cancellable: false
        }, async (progress) => {
            progress.report({ increment: 0 });
            
            try {
                // Call Claude API
                const response = await claudeService.explainCode(selectedText, language);
                progress.report({ increment: 100 });
                
                if (response.error) {
                    vscode.window.showErrorMessage(`Error: ${response.error}`);
                    return;
                }
                
                // Show response in webview panel
                showResponsePanel("Explain code", response.content, language);
            } catch (error) {
                vscode.window.showErrorMessage(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
            }
        });
    });
    
    context.subscriptions.push(getHelpCommand, explainCodeCommand);
}

// Create and show a webview panel with the response
function showResponsePanel(query: string, response: string, language?: string) {
    const panel = vscode.window.createWebviewPanel(
        'codingAssistant',
        'Coding Assistant',
        vscode.ViewColumn.Beside,
        {
            enableScripts: true
        }
    );
    
    panel.webview.html = getWebviewContent(query, response, language);
}

// Generate HTML for the webview panel
function getWebviewContent(query: string, response: string, language?: string) {
    return `<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Coding Assistant</title>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                padding: 20px; 
                color: var(--vscode-editor-foreground);
                background-color: var(--vscode-editor-background);
            }
            .query { 
                background-color: var(--vscode-editor-inactiveSelectionBackground);
                padding: 10px; 
                border-radius: 5px; 
                margin-bottom: 20px; 
            }
            .response { 
                white-space: pre-wrap;
                margin-bottom: 20px;
            }
            pre {
                background-color: var(--vscode-editor-lineHighlightBackground);
                padding: 10px;
                border-radius: 5px;
                overflow: auto;
            }
            code {
                font-family: 'SF Mono', Monaco, Menlo, Courier, monospace;
            }
            button {
                background-color: var(--vscode-button-background);
                color: var(--vscode-button-foreground);
                border: none;
                padding: 8px 12px;
                border-radius: 3px;
                cursor: pointer;
                margin-right: 5px;
            }
            button:hover {
                background-color: var(--vscode-button-hoverBackground);
            }
        </style>
    </head>
    <body>
        <h2>Coding Assistant</h2>
        <div class="query">
            <strong>Your query:</strong>
            <div>${query}</div>
        </div>
        <div class="response">
            <strong>Response:</strong>
            <div id="responseContent">${formatResponse(response)}</div>
        </div>
        <div>
            <button id="copyBtn">Copy Response</button>
            <button id="insertBtn">Insert at Cursor</button>
        </div>
        <script>
            const vscode = acquireVsCodeApi();
            
            document.getElementById('copyBtn').addEventListener('click', () => {
                const responseText = document.getElementById('responseContent').textContent;
                vscode.postMessage({
                    command: 'copy',
                    text: responseText
                });
            });
            
            document.getElementById('insertBtn').addEventListener('click', () => {
                const responseText = document.getElementById('responseContent').textContent;
                vscode.postMessage({
                    command: 'insert',
                    text: responseText
                });
            });
        </script>
    </body>
    </html>`;
}

// Format the response with markdown for code blocks
function formatResponse(text: string): string {
    // Convert markdown code blocks to HTML
    const formattedText = text.replace(/```([a-zA-Z]*)\n([\s\S]*?)```/g, (match, lang, code) => {
        return `<pre><code class="language-${lang}">${escapeHtml(code)}</code></pre>`;
    });
    
    // Convert line breaks to <br> tags
    return formattedText.replace(/\n/g, '<br>');
}

// Helper function to escape HTML
function escapeHtml(text: string): string {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

export function deactivate() {}