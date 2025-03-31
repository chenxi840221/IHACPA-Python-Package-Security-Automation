/**
 * GitHub Sync and Code Analysis Utility
 * 
 * This module provides functionality to sync with GitHub repositories
 * and analyze the source code for storage in a vector/knowledge store.
 */

const { exec } = require('child_process');
const fs = require('fs').promises;
const path = require('path');
const { promisify } = require('util');
const execPromise = promisify(exec);
const { OpenAIEmbeddings } = require('langchain/embeddings/openai');
const { HNSWLib } = require('langchain/vectorstores/hnswlib');
const { RecursiveCharacterTextSplitter } = require('langchain/text_splitter');

/**
 * Configuration for the GitHub sync and analysis
 */
const config = {
  tempDir: path.join(__dirname, 'temp_repos'),
  vectorStorePath: path.join(__dirname, 'vectorstore'),
  chunkSize: 1000,
  chunkOverlap: 200,
  openaiApiKey: process.env.OPENAI_API_KEY,
  fileExtensions: ['.js', '.jsx', '.ts', '.tsx', '.py', '.html', '.css', '.json', '.md'],
};

/**
 * Syncs a GitHub repository (clone and push) and analyzes the code for vector storage
 * 
 * @param {string} repoUrl - The URL of the GitHub repository to sync
 * @param {string} branch - The branch to sync (default: 'main')
 * @param {string} localDir - Optional specific directory name within tempDir
 * @returns {Promise<string>} - The path to the created vector store
 */
async function syncAndAnalyzeRepo(repoUrl, branch = 'main', localDir = null) {
  try {
    // Extract repo name from URL
    const repoName = repoUrl.split('/').pop().replace('.git', '');
    const repoDir = localDir || `${repoName}_${Date.now()}`;
    const fullRepoPath = path.join(config.tempDir, repoDir);
    
    console.log(`Starting sync and analysis for ${repoUrl}`);
    
    // Create temp directory if it doesn't exist
    await fs.mkdir(config.tempDir, { recursive: true });
    
    // Clone the repository
    console.log(`Cloning repository to ${fullRepoPath}...`);
    await execPromise(`git clone ${repoUrl} -b ${branch} ${fullRepoPath}`);
    
    // Pull latest changes if repo already exists
    try {
      console.log('Pulling latest changes...');
      await execPromise(`cd ${fullRepoPath} && git pull origin ${branch}`);
    } catch (pullError) {
      console.warn('Pull failed, continuing with existing code:', pullError.message);
    }
    
    // Analyze the code
    console.log('Analyzing code...');
    const sourceCode = await loadSourceCode(fullRepoPath);
    
    // Process and store in vector database
    console.log('Processing and storing code in vector database...');
    const vectorStorePath = await processAndStoreCode(sourceCode, repoName);
    
    console.log(`Repository synced and analyzed successfully. Vector store at: ${vectorStorePath}`);
    return vectorStorePath;
  } catch (error) {
    console.error('Error in syncAndAnalyzeRepo:', error);
    throw error;
  }
}

/**
 * Recursively loads all source code from a directory
 * 
 * @param {string} dir - Directory to load source code from
 * @returns {Promise<Array<{path: string, content: string}>>} - Array of file paths and contents
 */
async function loadSourceCode(dir) {
  const results = [];
  
  async function processDir(currentDir) {
    const entries = await fs.readdir(currentDir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);
      
      // Skip node_modules, .git directories, and other common non-source folders
      if (entry.isDirectory()) {
        if (!['.git', 'node_modules', 'dist', 'build', '.cache'].includes(entry.name)) {
          await processDir(fullPath);
        }
        continue;
      }
      
      // Only process files with specified extensions
      const ext = path.extname(entry.name).toLowerCase();
      if (config.fileExtensions.includes(ext)) {
        try {
          const content = await fs.readFile(fullPath, 'utf8');
          results.push({
            path: fullPath,
            content,
          });
        } catch (error) {
          console.warn(`Error reading file ${fullPath}:`, error.message);
        }
      }
    }
  }
  
  await processDir(dir);
  return results;
}

/**
 * Process and store code in a vector database
 * 
 * @param {Array<{path: string, content: string}>} sourceFiles - Array of source files
 * @param {string} repoName - Name of the repository
 * @returns {Promise<string>} - Path to the vector store
 */
async function processAndStoreCode(sourceFiles, repoName) {
  // Initialize text splitter
  const textSplitter = new RecursiveCharacterTextSplitter({
    chunkSize: config.chunkSize,
    chunkOverlap: config.chunkOverlap,
  });
  
  // Combine all files with metadata
  const documents = [];
  
  for (const file of sourceFiles) {
    const chunks = await textSplitter.createDocuments(
      [file.content],
      [{ 
        source: file.path,
        type: path.extname(file.path).substring(1), // Remove the dot from extension
        repoName: repoName
      }]
    );
    documents.push(...chunks);
  }
  
  // Initialize embeddings
  const embeddings = new OpenAIEmbeddings({
    openAIApiKey: config.openaiApiKey,
  });
  
  // Define the specific vector store path for this repo
  const repoVectorStorePath = path.join(config.vectorStorePath, repoName);
  
  // Create directory if it doesn't exist
  await fs.mkdir(repoVectorStorePath, { recursive: true });
  
  // Create and save the vector store
  const vectorStore = await HNSWLib.fromDocuments(documents, embeddings);
  await vectorStore.save(repoVectorStorePath);
  
  return repoVectorStorePath;
}

/**
 * Push changes to the GitHub repository
 * 
 * @param {string} repoPath - Path to the local repository
 * @param {string} commitMessage - Commit message
 * @param {string} branch - Branch to push to (default: 'main')
 * @returns {Promise<void>}
 */
async function pushChanges(repoPath, commitMessage, branch = 'main') {
  try {
    console.log(`Pushing changes to ${branch} with message: ${commitMessage}`);
    
    // Add all changes
    await execPromise(`cd ${repoPath} && git add .`);
    
    // Commit changes
    await execPromise(`cd ${repoPath} && git commit -m "${commitMessage}"`);
    
    // Push to remote
    await execPromise(`cd ${repoPath} && git push origin ${branch}`);
    
    console.log('Changes pushed successfully');
  } catch (error) {
    console.error('Error pushing changes:', error);
    throw error;
  }
}

module.exports = {
  syncAndAnalyzeRepo,
  pushChanges,
};