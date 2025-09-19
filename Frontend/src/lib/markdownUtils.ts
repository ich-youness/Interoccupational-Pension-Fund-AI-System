/**
 * Utility functions for formatting and processing markdown content from agents
 */

/**
 * Cleans and formats markdown content from agent responses
 * @param content - Raw markdown content from agent
 * @returns Cleaned and formatted markdown content
 */
export const formatAgentOutput = (content: string): string => {
  if (!content) return '';

  let formatted = content;

  // Remove excessive newlines (more than 2 consecutive)
  formatted = formatted.replace(/\n{3,}/g, '\n\n');

  // Ensure proper spacing around headers
  formatted = formatted.replace(/(\n|^)(#{1,6}\s+)/g, '\n\n$2');
  formatted = formatted.replace(/(#{1,6}[^\n]+)\n([^#\n])/g, '$1\n\n$2');

  // Ensure proper spacing around code blocks
  formatted = formatted.replace(/(\n|^)(```[\s\S]*?```)/g, '\n\n$2');
  formatted = formatted.replace(/(```[\s\S]*?```)(\n)([^`\n])/g, '$1\n\n$3');

  // Ensure proper spacing around lists
  formatted = formatted.replace(/(\n|^)([\*\-\+]\s+)/g, '\n$2');
  formatted = formatted.replace(/(\n|^)(\d+\.\s+)/g, '\n$2');

  // Clean up excessive horizontal rules
  formatted = formatted.replace(/(\n|^)(-{3,})(\n|$)/g, '\n\n---\n\n');

  // Remove leading/trailing whitespace
  formatted = formatted.trim();

  return formatted;
};

/**
 * Extracts key sections from agent output for quick preview
 * @param content - Full markdown content
 * @returns Object with extracted sections
 */
export const extractSections = (content: string) => {
  const sections: { [key: string]: string } = {};
  
  // Extract headers and their content
  const headerRegex = /^(#{1,6})\s+(.+)$/gm;
  let match;
  let currentSection = '';
  let currentHeader = '';

  const lines = content.split('\n');
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const headerMatch = line.match(/^(#{1,6})\s+(.+)$/);
    
    if (headerMatch) {
      // Save previous section
      if (currentHeader && currentSection) {
        sections[currentHeader] = currentSection.trim();
      }
      
      // Start new section
      currentHeader = headerMatch[2].replace(/\*\*/g, '').trim();
      currentSection = '';
    } else {
      currentSection += line + '\n';
    }
  }
  
  // Save last section
  if (currentHeader && currentSection) {
    sections[currentHeader] = currentSection.trim();
  }
  
  return sections;
};

/**
 * Creates a table of contents from markdown headers
 * @param content - Markdown content
 * @returns Array of TOC items
 */
export const generateTableOfContents = (content: string) => {
  const toc: Array<{ level: number; title: string; id: string }> = [];
  
  const headerRegex = /^(#{1,6})\s+(.+)$/gm;
  let match;
  
  while ((match = headerRegex.exec(content)) !== null) {
    const level = match[1].length;
    const title = match[2].replace(/\*\*/g, '').trim();
    const id = title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    
    toc.push({ level, title, id });
  }
  
  return toc;
};

/**
 * Validates if content is valid markdown
 * @param content - Content to validate
 * @returns Boolean indicating if content appears to be markdown
 */
export const isMarkdownContent = (content: string): boolean => {
  if (!content) return false;
  
  // Check for common markdown patterns
  const markdownPatterns = [
    /^#{1,6}\s+/m,           // Headers
    /\*\*.*?\*\*/,           // Bold text
    /\*.*?\*/,               // Italic text
    /```[\s\S]*?```/,        // Code blocks
    /`[^`]+`/,               // Inline code
    /^\s*[\*\-\+]\s+/m,      // Unordered lists
    /^\s*\d+\.\s+/m,         // Ordered lists
    /^\s*>\s+/m,             // Blockquotes
    /\[.*?\]\(.*?\)/,        // Links
    /^\s*\|.*\|/m,           // Tables
    /^---+$/m,               // Horizontal rules
  ];
  
  return markdownPatterns.some(pattern => pattern.test(content));
};

/**
 * Truncates markdown content while preserving structure
 * @param content - Full markdown content
 * @param maxLength - Maximum character length
 * @returns Truncated content with ellipsis
 */
export const truncateMarkdown = (content: string, maxLength: number = 500): string => {
  if (content.length <= maxLength) return content;
  
  // Find a good breaking point (end of sentence, paragraph, or section)
  const truncated = content.substring(0, maxLength);
  const lastSentence = truncated.lastIndexOf('.');
  const lastParagraph = truncated.lastIndexOf('\n\n');
  const lastSection = truncated.lastIndexOf('\n###');
  
  const breakPoint = Math.max(lastSentence, lastParagraph, lastSection);
  
  if (breakPoint > maxLength * 0.7) {
    return content.substring(0, breakPoint + 1) + '\n\n...';
  }
  
  return truncated + '...';
};
