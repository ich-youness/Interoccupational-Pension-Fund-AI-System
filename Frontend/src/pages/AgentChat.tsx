import { useState, useRef, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { ChevronLeft, Send, Bot, User, Users, Loader2, ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";
import { scenarioOptimizationTeam, allTeams } from "@/data/Modules";
import React from "react";
import ReactMarkdown from "react-markdown";


const defaultAgents = [
  "React Specialist",
  "UX Expert", 
  "TypeScript Pro",
  "API Architect",
  "Database Expert",
  "Security Specialist"
];

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'agent';
  agentName?: string;
  timestamp: Date;
  isLoading?: boolean;
  images?: string[];
}

const AgentChat = () => {
  const { teamId, subTeamId } = useParams();
  
  // Get all agents from all teams
  const getAllAgents = () => {
    const allAgents: { agent: any; teamId: string; subTeamId: string }[] = [];
    allTeams.forEach(team => {
      team.subTeams.forEach(subTeam => {
        subTeam.agents.forEach(agent => {
          allAgents.push({
            agent,
            teamId: team.id,
            subTeamId: subTeam.id
          });
        });
      });
    });
    return allAgents;
  };
  
  const allAgents = getAllAgents();
  const [selectedAgent, setSelectedAgent] = useState<{ agent: any; teamId: string; subTeamId: string } | null>(
    allAgents.length > 0 ? allAgents[0] : null
  );
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: `Hello! I'm ${allAgents[0]?.agent.name || 'Assistant'}. How can I help you today?`,
      sender: 'agent',
      agentName: allAgents[0]?.agent.name || 'Assistant',
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  const callBackendAPI = async (prompt: string, agentId: string) => {
    try {
      const requestBody = {
        moduleId: selectedAgent.teamId === 'fip-ai' ? 'fip-ai' : 'scenario-optimization',
        agentId: agentId,
        prompt: prompt + (selectedAgent.teamId === 'fip-ai' ? "" : " here is the excel file path: D:/Assurance_OS/Backend/Agent_V2/Inputs/Template_scenario_mix_P&C2.xlsx"),
        config: {}
      };
      
      console.log('Making API call with:', requestBody);
      console.log('Selected agent:', selectedAgent);
      
      const response = await fetch('http://127.0.0.1:8000/module', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      console.log('Response status:', response.status);
      console.log('Response headers:', response.headers);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Response error:', errorText);
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }

      const data = await response.json();
      console.log('Response data:', data);
      return data;
    } catch (error) {
      console.error('Error calling backend API:', error);
      throw error;
    }
  };

  // Function to extract image filenames from agent response
  const extractImageFilenames = (text: string): string[] => {
    // More robust regex to match PNG filenames with various patterns including spaces and parentheses
    // Look for patterns like: plot_metric_timestamp.png or any filename ending in .png
    const imageRegex = /([a-zA-Z0-9_\-\.\s\(\)]+\.png)/g;
    const matches = text.match(imageRegex);
    
    // Also try to find filenames in markdown image syntax: ![alt](filename.png)
    const markdownImageRegex = /!\[.*?\]\(([^)]+\.png)\)/g;
    const markdownMatches = text.match(markdownImageRegex);
    
    let allMatches: string[] = matches || [];
    if (markdownMatches) {
      const markdownFilenames = markdownMatches.map(match => {
        const filenameMatch = match.match(/!\[.*?\]\(([^)]+\.png)\)/);
        return filenameMatch ? filenameMatch[1] : null;
      }).filter(Boolean) as string[];
      allMatches = [...allMatches, ...markdownFilenames];
    }
    
    // Fix truncated filenames - if we find a filename that looks truncated (starts with number and parentheses)
    // try to find the full filename in the text
    allMatches = allMatches.map(filename => {
      // Check if filename looks truncated (starts with number and parentheses like "20(central)_timestamp.png")
      const truncatedPattern = /^\d+\([^)]+\)_\d{8}_\d{6}\.png$/;
      if (truncatedPattern.test(filename)) {
        // Try to find the full filename in the text by looking for plot_* patterns with the same timestamp
        const timestamp = filename.split('_')[1] + '_' + filename.split('_')[2];
        const fullFilenamePattern = new RegExp(`plot_[^\\s]+\\s+[^\\s]+\\s+[^\\s]+\\s+\\([^)]+\\)_${timestamp}\\.png`, 'i');
        const fullMatch = text.match(fullFilenamePattern);
        if (fullMatch) {
          console.log('Found full filename for truncated:', filename, '->', fullMatch[0]);
          return fullMatch[0];
        }
        
        // If not found, try a simpler pattern - look for any plot_* file with the same timestamp
        const simplePattern = new RegExp(`plot_[^\\s]+\\s+[^\\s]+\\s+[^\\s]+\\s+\\([^)]+\\)_${timestamp}\\.png`, 'i');
        const simpleMatch = text.match(simplePattern);
        if (simpleMatch) {
          console.log('Found full filename (simple pattern):', filename, '->', simpleMatch[0]);
          return simpleMatch[0];
        }
      }
      return filename;
    });
    
    // Debug logging
    console.log('Extracted image filenames:', allMatches);
    console.log('Original text snippet:', text.substring(0, 500));
    
    return allMatches;
  };

  // Function to check if response contains images
  const hasImages = (text: string): boolean => {
    return extractImageFilenames(text).length > 0;
  };

  // ImageDisplay component
  const ImageDisplay = ({ images }: { images: string[] }) => {
    return (
      <div className="mt-4 space-y-3">
        {images.map((filename, index) => (
          <div key={index} className="border border-third-color/20 rounded-lg p-3 bg-fourth-color/5">
            <div className="flex items-center gap-2 mb-2">
              <div className="w-2 h-2 bg-green-400 rounded-full"></div>
              <span className="text-sm text-fourth-color/70">Generated Visualization</span>
            </div>
            <img
              src={`http://127.0.0.1:8000/images/${encodeURIComponent(filename)}`}
              alt={`Generated visualization ${index + 1}`}
              className="max-w-full h-auto rounded border border-third-color/20"
              onError={(e) => {
                console.error(`Failed to load image: ${filename}`);
                // Try alternative filename patterns if the original fails
                const timestamp = filename.match(/(\d{8}_\d{6})\.png$/);
                if (timestamp) {
                  const altFilename = `plot_IFRS Capital (central)_${timestamp[1]}.png`;
                  console.log(`Trying alternative filename: ${altFilename}`);
                  e.currentTarget.src = `http://127.0.0.1:8000/images/${encodeURIComponent(altFilename)}`;
                } else {
                  e.currentTarget.style.display = 'none';
                }
              }}
            />
            <p className="text-xs text-fourth-color/50 mt-1">{filename}</p>
          </div>
        ))}
      </div>
    );
  };


  // from gpt: convert markdown to html
  const MarkdownRenderer = ({ content }: { content: string }) => {
    return (
      <div className="prose prose-invert max-w-none">
        <ReactMarkdown>{content}</ReactMarkdown>
      </div>
    );
  };

  // function markdownToHTML(markdown: string): string {
  //   let html = markdown;
  
  //   // Escape newlines properly
  //   html = html.replace(/\\n/g, "\n");
  
  //   // Headings (###, ##, #)
  //   html = html.replace(/^###\s\*\*(.+?)\*\*/gm, "<h3><strong>$1</strong></h3>");
  //   html = html.replace(/^###\s(.+)$/gm, "<h3>$1</h3>");
  //   html = html.replace(/^##\s(.+)$/gm, "<h2>$1</h2>");
  //   html = html.replace(/^#\s(.+)$/gm, "<h1>$1</h1>");
  
  //   // Bold (**text**)
  //   html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  
  //   // Inline code (`text`)
  //   html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
  
  //   // Code blocks (```json ... ```)
  //   html = html.replace(/```json\n([\s\S]*?)```/g, "<pre><code class='language-json'>$1</code></pre>");
  //   html = html.replace(/```([\s\S]*?)```/g, "<pre><code>$1</code></pre>");
  
  //   // Unordered lists (- item)
  //   html = html.replace(/^- (.+)$/gm, "<li>$1</li>");
  //   html = html.replace(/(<li>.*<\/li>)/gs, "<ul>$1</ul>");
  
  //   // Horizontal rules (---)
  //   html = html.replace(/---/g, "<hr />");
  
  //   // Markdown tables
  //   html = html.replace(
  //     /\|(.+)\|\n\|([\s\-:|]+)\|\n([\s\S]+?)(?=\n\n|$)/g,
  //     (match, headerRow, divider, bodyRows) => {
  //       const headers = headerRow
  //         .split("|")
  //         .map((h: string) => `<th>${h.trim()}</th>`)
  //         .join("");
  
  //       const rows = bodyRows
  //         .trim()
  //         .split("\n")
  //         .map((row: string) => {
  //           const cells = row
  //             .split("|")
  //             .map((c: string) => `<td>${c.trim()}</td>`)
  //             .join("");
  //           return `<tr>${cells}</tr>`;
  //         })
  //         .join("");
  
  //       return `<table><thead><tr>${headers}</tr></thead><tbody>${rows}</tbody></table>`;
  //     }
  //   );
  
  //   // Paragraphs (anything not wrapped)
  //   html = html.replace(/^(?!<[hruolp]|<pre|<table)(.+)$/gm, "<p>$1</p>");
  
  //   return html;
  // }
  

  // API call function
  
  // function markdownToHTML(markdown: string): string {
  //   let html = markdown;
  
  //   // Fix newlines
  //   html = html.replace(/\\n/g, "\n");
  
  //   // Headings
  //   html = html.replace(/^###\s?(.+)$/gm, "<h3>$1</h3>");
  //   html = html.replace(/^##\s?(.+)$/gm, "<h2>$1</h2>");
  //   html = html.replace(/^#\s?(.+)$/gm, "<h1>$1</h1>");
  //   // Numbered section titles (e.g. "1. Data Quality Assessment")
  //   html = html.replace(/^\d+\.\s?(.+)$/gm, "<h3>$1</h3>");
  
  //   // Bold text
  //   html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  
  //   // Inline code
  //   html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
  
  //   // Code blocks
  //   html = html.replace(/```json\n([\s\S]*?)```/g, "<pre><code class='language-json'>$1</code></pre>");
  //   html = html.replace(/```([\s\S]*?)```/g, "<pre><code>$1</code></pre>");
  
  //   // Lists
  //   html = html.replace(/^- (.+)$/gm, "<li>$1</li>");
  //   html = html.replace(/(<li>[\s\S]*?<\/li>)/gm, "<ul>$1</ul>");
  
  //   // Horizontal rules
  //   html = html.replace(/^---$/gm, "<hr />");
  
  //   // Tables
  //   html = html.replace(
  //     /\|(.+)\|\n\|([\s\-:|]+)\|\n([\s\S]+?)(?=\n\n|$)/g,
  //     (match, headerRow, divider, bodyRows) => {
  //       const headers = headerRow
  //         .split("|")
  //         .map((h: string) => `<th>${h.trim()}</th>`)
  //         .join("");
  
  //       const rows = bodyRows
  //         .trim()
  //         .split("\n")
  //         .map((row: string) => {
  //           const cells = row
  //             .split("|")
  //             .map((c: string) => `<td>${c.trim()}</td>`)
  //             .join("");
  //           return `<tr>${cells}</tr>`;
  //         })
  //         .join("");
  
  //       return `<table class="table-auto border-collapse border border-gray-500 my-4"><thead><tr>${headers}</tr></thead><tbody>${rows}</tbody></table>`;
  //     }
  //   );
  
  //   // Wrap standalone lines into paragraphs
  //   html = html.replace(/^(?!<h\d>|<ul>|<li>|<pre>|<table>|<hr)(.+)$/gm, "<p>$1</p>");
  
  //   return html;
  // }
  

  // Function to convert JSON to readable HTML
  const convertJsonToHtml = (data: any): string => {
    if (Array.isArray(data)) {
      // Handle arrays - create a table if objects, or list if primitives
      if (data.length > 0 && typeof data[0] === 'object' && data[0] !== null) {
        // Array of objects - create table
        const keys = Object.keys(data[0]);
        const headerRow = keys.map(key => `<th class="border border-gray-400 px-3 py-2 bg-gray-700 text-white font-semibold">${key.replace(/_/g, ' ')}</th>`).join('');
        const bodyRows = data.map(item => 
          `<tr>${keys.map(key => `<td class="border border-gray-400 px-3 py-2 text-white">${formatValue(item[key])}</td>`).join('')}</tr>`
        ).join('');
        return `<div class="my-4"><h4 class="text-white font-semibold mb-2">Data Records (${data.length} items)</h4><table class="table-auto border-collapse border border-gray-400 w-full"><thead><tr>${headerRow}</tr></thead><tbody>${bodyRows}</tbody></table></div>`;
      } else {
        // Array of primitives - create list
        const listItems = data.map(item => `<li class="text-white">${formatValue(item)}</li>`).join('');
        return `<div class="my-4"><h4 class="text-white font-semibold mb-2">List (${data.length} items)</h4><ul class="list-disc list-inside space-y-1">${listItems}</ul></div>`;
      }
    } else if (typeof data === 'object' && data !== null) {
      // Handle objects - create key-value pairs
      const entries = Object.entries(data);
      const rows = entries.map(([key, value]) => 
        `<tr><td class="border border-gray-400 px-3 py-2 bg-gray-700 text-white font-semibold">${key.replace(/_/g, ' ')}</td><td class="border border-gray-400 px-3 py-2 text-white">${formatValue(value)}</td></tr>`
      ).join('');
      return `<div class="my-4"><h4 class="text-white font-semibold mb-2">Data Details</h4><table class="table-auto border-collapse border border-gray-400 w-full"><tbody>${rows}</tbody></table></div>`;
    } else {
      // Primitive value
      return `<div class="my-4 p-3 bg-gray-800 rounded border text-white"><strong>Value:</strong> ${formatValue(data)}</div>`;
    }
  };

  const formatValue = (value: any): string => {
    if (value === null) return '<em class="text-gray-400">null</em>';
    if (value === undefined) return '<em class="text-gray-400">undefined</em>';
    if (typeof value === 'boolean') return `<span class="text-blue-400">${value}</span>`;
    if (typeof value === 'number') return `<span class="text-green-400">${value.toLocaleString()}</span>`;
    if (typeof value === 'string') {
      // Check if it's a date
      if (/^\d{4}-\d{2}-\d{2}/.test(value)) {
        return `<span class="text-yellow-400">${value}</span>`;
      }
      return value;
    }
    if (Array.isArray(value)) {
      return `<span class="text-purple-400">Array (${value.length} items)</span>`;
    }
    if (typeof value === 'object') {
      return `<span class="text-orange-400">Object (${Object.keys(value).length} properties)</span>`;
    }
    return String(value);
  };

  function markdownToHTML(markdown: string): string {
    let html = markdown;
  
    // Fix newlines
    html = html.replace(/\\n/g, "\n");
  
    // Headings
    html = html.replace(/^###\s?(.+)$/gm, "<h3>$1</h3>");
    html = html.replace(/^##\s?(.+)$/gm, "<h2>$1</h2>");
    html = html.replace(/^#\s?(.+)$/gm, "<h1>$1</h1>");
    html = html.replace(/^\d+\.\s?(.+)$/gm, "<h3>$1</h3>");
  
    // Bold
    html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  
    // Inline code
    html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
  
         // Code blocks - handle JSON and other code
     html = html.replace(/```json\n([\s\S]*?)```/g, (match, code) => {
       // Clean up escaped quotes and format JSON
       let cleanCode = code.replace(/\\"/g, '"').replace(/\\n/g, '\n');
       try {
         // Try to parse JSON and convert to readable HTML
         const parsed = JSON.parse(cleanCode);
         return convertJsonToHtml(parsed);
       } catch (e) {
         // If parsing fails, just use the cleaned code in a code block
         return `<pre class="bg-gray-800 text-white p-4 rounded-lg overflow-x-auto my-4"><code class="language-json text-sm text-white">${cleanCode}</code></pre>`;
       }
     });
     
     html = html.replace(/```([\s\S]*?)```/g, (match, code) => {
       // Clean up escaped quotes for non-JSON code blocks
       const cleanCode = code.replace(/\\"/g, '"').replace(/\\n/g, '\n');
       return `<pre class="bg-gray-800 text-white p-4 rounded-lg overflow-x-auto my-4"><code class="text-sm text-white">${cleanCode}</code></pre>`;
     });
  
    // Lists
    html = html.replace(/^- (.+)$/gm, "<li>$1</li>");
    html = html.replace(/(<li>[\s\S]*?<\/li>)/gm, "<ul>$1</ul>");
  
    // Horizontal rules
    html = html.replace(/^---$/gm, "<hr />");
  
         // Standard markdown tables (| column | column |)
     html = html.replace(
       /(\|.+\|\n\|[\s\-:|]+\|\n[\s\S]+?)(?=\n\n|\n[^|]|$)/g,
       (match) => {
         const lines = match.trim().split('\n');
         if (lines.length < 2) return match;
         
         const headerRow = lines[0];
         const separatorRow = lines[1];
         const bodyRows = lines.slice(2);
         
         // Parse header
         const headers = headerRow
           .split('|')
           .map(h => h.trim())
           .filter(h => h.length > 0)
           .map(h => `<th class="border border-gray-400 px-2 py-1">${h}</th>`)
           .join('');
         
         // Parse body rows
         const rows = bodyRows
           .map(row => {
             const cells = row
               .split('|')
               .map(c => c.trim())
               .filter(c => c.length > 0)
               .map(c => `<td class="border border-gray-400 px-2 py-1">${c}</td>`)
               .join('');
             return `<tr>${cells}</tr>`;
           })
           .join('');
         
         return `<table class="table-auto border-collapse border border-gray-400 my-4 w-full"><thead><tr>${headers}</tr></thead><tbody>${rows}</tbody></table>`;
       }
     );
  
    // Wrap paragraphs
    html = html.replace(/^(?!<h\d>|<ul>|<li>|<pre>|<table>|<hr)(.+)$/gm, "<p>$1</p>");
  
    return html;
  }
  


  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Update selected agent when agents change
  useEffect(() => {
    if (allAgents.length > 0 && !selectedAgent) {
      setSelectedAgent(allAgents[0]);
      const welcomeMessage: Message = {
        id: Date.now().toString(),
        content: `Hello! I'm ${allAgents[0].agent.name}. I'm now ready to assist you.`,
        sender: 'agent',
        agentName: allAgents[0].agent.name,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, welcomeMessage]);
    }
  }, [allAgents, selectedAgent]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputMessage,
      sender: 'user',
      timestamp: new Date()
    };

    // Store the message content before clearing the input
    const messageContent = inputMessage;
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      if (!selectedAgent) return;
      
      // Get the agent ID from the selected agent
      const agentId = selectedAgent.agent.id;
      
      // Call the backend API with the stored message content
      const response = await callBackendAPI(messageContent, agentId);
      
      // Extract response content and images
      const responseContent = response.response || response;
      const images = extractImageFilenames(responseContent);
      
      const agentResponse: Message = {
        id: (Date.now() + 1).toString(),
        content: responseContent,
        sender: 'agent',
        agentName: selectedAgent.agent.name,
        timestamp: new Date(),
        images: images.length > 0 ? images : undefined
      };
      setMessages(prev => [...prev, agentResponse]);
    } catch (error) {
      console.error('Error getting agent response:', error);
      
      // Fallback response if API fails
      const errorResponse: Message = {
        id: (Date.now() + 1).toString(),
        content: `Sorry, I'm having trouble connecting to the server right now. Please try again later.`,
        sender: 'agent',
        agentName: selectedAgent?.agent.name || 'Assistant',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorResponse]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAgentChange = (agentData: { agent: any; teamId: string; subTeamId: string }) => {
    setSelectedAgent(agentData);
    
    const agent = agentData.agent;
    let welcomeContent = `Hello! I'm ${agent.name}. I'm now ready to assist you.`;
    
    // Add specific welcome for agents
    if (agent.description) {
      welcomeContent = `Hello! I'm ${agent.name}. ${agent.description}. I specialize in: ${agent.outputs.slice(0, 3).join(', ')}. How can I help you today?`;
    }
    
    const welcomeMessage: Message = {
      id: Date.now().toString(),
      content: welcomeContent,
      sender: 'agent',
      agentName: agent.name,
      timestamp: new Date()
    };
    
    // Reset chat history and add only the welcome message
    setMessages([welcomeMessage]);
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="h-screen bg-background flex">
      {/* Left Sidebar - Agents */}
      <div className="w-1/4 bg-second-color border-r border-third-color/20 flex flex-col">
        {/* Sidebar Header */}
        <div className="p-4 border-b border-third-color/20">
          <Link to={`/team/${teamId}`}>
            <Button variant="ghost" size="sm" className="text-fourth-color hover:bg-third-color mb-3">
              <ChevronLeft className="h-4 w-4 mr-2" />
              Back
            </Button>
          </Link>
          <div className="flex items-center gap-2 text-fourth-color">
            <Users className="h-5 w-5" />
            <h2 className="font-semibold">Team Agents</h2>
          </div>
        </div>

        {/* Teams and Agents List */}
        <div className="flex-1 overflow-y-auto p-4">
          <Accordion type="multiple" className="w-full">
            {allTeams.map((team) => (
              <AccordionItem key={team.id} value={team.id} className="border-none">
                <AccordionTrigger className="py-3 px-0 text-fourth-color hover:text-first-color hover:no-underline">
                  <div className="flex items-center gap-2">
                    <team.icon className="h-4 w-4" />
                    <span className="font-medium">{team.name}</span>
                  </div>
                </AccordionTrigger>
                <AccordionContent className="pb-2">
                  <div className="space-y-1 ml-6">
                    {team.subTeams.map((subTeam) => (
                      <div key={subTeam.id} className="space-y-1">
                        <div className="flex items-center gap-2 text-fourth-color/70 text-sm font-medium py-1">
                          <subTeam.icon className="h-3 w-3" />
                          <span>{subTeam.name}</span>
                        </div>
                        <div className="space-y-1 ml-4">
                          {subTeam.agents.map((agent) => (
                            <Button
                              key={agent.id}
                              variant="ghost"
                              size="sm"
                              className={cn(
                                "w-full justify-start transition-smooth text-fourth-color text-xs h-8",
                                selectedAgent?.agent.id === agent.id 
                                  ? "bg-third-color text-first-color" 
                                  : "hover:bg-third-color/20"
                              )}
                              onClick={() => handleAgentChange({ agent, teamId: team.id, subTeamId: subTeam.id })}
                            >
                              <Bot className="h-3 w-3 mr-2" />
                              {agent.name}
                            </Button>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      </div>

      {/* Right Main Content - Chat */}
      <div className="flex-1 flex flex-col">
        {/* Chat Header */}
        <div className="bg-first-color p-4 border-b border-third-color/20">
          <div className="flex items-center gap-3">
            <Bot className="h-6 w-6 text-fourth-color" />
            <div>
              <h1 className="text-xl font-semibold text-fourth-color">
                {selectedAgent?.agent.name || 'Assistant'}
              </h1>
              <p className="text-fourth-color/70 text-sm">
                AI Assistant • Online
              </p>
            </div>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={cn(
                "flex items-start gap-3",
                message.sender === 'user' ? "justify-end" : "justify-start"
              )}
            >
              {message.sender === 'agent' && (
                <div className="w-8 h-8 rounded-full bg-third-color flex items-center justify-center flex-shrink-0">
                  <Bot className="h-4 w-4 text-first-color" />
                  
                </div>
              )}
              
              <Card className={cn(
                "max-w-[70%] p-4 border-0",
                message.sender === 'user' 
                  ? "bg-third-color text-first-color" 
                  : "bg-fourth-color text-first-color"
              )}>
                {message.sender === 'agent' && (
                  <p className="text-xs font-medium text-first-color/70 mb-1">
                    {message.agentName}
                    

                  </p>
                )}
                <div
                  className="text-sm max-w-none text-white [&>*]:text-white [&>h1]:text-white [&>h2]:text-white [&>h3]:text-white [&>p]:text-white [&>li]:text-white [&>code]:text-white [&>pre]:text-white [&>strong]:text-white [&>table]:text-white [&>th]:text-white [&>td]:text-white"
                  dangerouslySetInnerHTML={{ __html: markdownToHTML(message.content) }}
                />
                {message.images && message.images.length > 0 && (
                  <ImageDisplay images={message.images} />
                )}
                <p className="text-xs text-first-color/50 mt-2">
                  {formatTime(message.timestamp)}
                </p>
              </Card>

              {message.sender === 'user' && (
                <div className="w-8 h-8 rounded-full bg-fourth-color flex items-center justify-center flex-shrink-0">
                  <User className="h-4 w-4 text-first-color" />
                </div>
              )}
            </div>
          ))}
          
          {/* Loading indicator */}
          {isLoading && (
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-full bg-third-color flex items-center justify-center flex-shrink-0">
                <Bot className="h-4 w-4 text-first-color" />
              </div>
              <Card className="max-w-[70%] p-4 border-0 bg-fourth-color text-first-color">
                <p className="text-xs font-medium text-first-color/70 mb-1">
                  {selectedAgent?.agent.name || 'Assistant'}
                </p>
                <div className="flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <p className="text-sm">Thinking...</p>
                </div>
              </Card>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-6 border-t border-third-color/20 bg-second-color/50">
          <div className="flex gap-3">
            <Input
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 bg-background border-third-color/20 text-foreground placeholder:text-muted-foreground focus:border-third-color"
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            />
            <Button
              onClick={handleSendMessage}
              className="bg-third-color hover:bg-third-color/80 text-first-color"
              disabled={!inputMessage.trim()}
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgentChat; 
