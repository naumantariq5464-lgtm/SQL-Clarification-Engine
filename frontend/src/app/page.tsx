"use client";

import { useState, useRef, useEffect } from "react";
import { Send, User, Bot, AlertCircle, Database, CheckCircle2 } from "lucide-react";

interface Message {
  role: "user" | "ai";
  content: string;
  isClarification?: boolean;
  accuracyScore?: number | null;
  sql?: string | null;
}

export default function Home() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    { role: "ai", content: "Hello! I am your Database Assistant. Ask me anything about your customers, orders, or products." }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  useEffect(() => scrollToBottom(), [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMessage: Message = { role: "user", content: input };
    const chatHistory = messages.map(m => ({ role: m.role, content: m.content }));
    
    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          question: userMessage.content,
          history: chatHistory
        }),
      });

      if (!response.ok) throw new Error("Failed to fetch");
      
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      
      if (!reader) throw new Error("No reader");
      
      let done = false;
      let aiContent = "";
      let aiMessageAdded = false;
      
      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        if (value) {
          const chunkStr = decoder.decode(value, { stream: true });
          const lines = chunkStr.split('\n');
          
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const dataStr = line.replace('data: ', '').trim();
              if (!dataStr) continue;
              
              try {
                const data = JSON.parse(dataStr);
                
                // Add AI message bubble only when we receive the first piece of data
                if (!aiMessageAdded) {
                  aiMessageAdded = true;
                  setIsLoading(false);
                  setMessages(prev => [...prev, { role: "ai", content: "" }]);
                }
                
                if (data.type === 'metadata') {
                  setMessages(prev => {
                    const newMessages = [...prev];
                    const lastMsg = newMessages[newMessages.length - 1];
                    lastMsg.isClarification = data.needs_clarification;
                    lastMsg.accuracyScore = data.accuracy_score;
                    lastMsg.sql = data.sql;
                    return newMessages;
                  });
                } else if (data.type === 'token') {
                  aiContent += data.content;
                  setMessages(prev => {
                    const newMessages = [...prev];
                    const lastMsg = newMessages[newMessages.length - 1];
                    lastMsg.content = aiContent;
                    return newMessages;
                  });
                } else if (data.type === 'error') {
                   aiContent += `\nError: ${data.content}`;
                   setMessages(prev => {
                      const newMessages = [...prev];
                      const lastMsg = newMessages[newMessages.length - 1];
                      lastMsg.content = aiContent;
                      return newMessages;
                   });
                }
              } catch (e) {
                console.error("Error parsing SSE JSON:", e);
              }
            }
          }
        }
      }
    } catch (error) {
      setMessages(prev => [...prev, { role: "ai", content: "Oops! Something went wrong connecting to the server." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-white text-black font-sans">
      
      {/* Header */}
      <header className="flex items-center justify-center py-5 border-b border-gray-200">
        <h1 className="text-xl font-bold tracking-tight">SQL Clarification Engine</h1>
      </header>

      {/* Chat Area */}
      <main className="flex-1 overflow-y-auto p-4 md:p-8">
        <div className="max-w-3xl mx-auto space-y-6">
          {messages.map((msg, index) => (
            <div key={index} className={`flex gap-4 ${msg.role === "user" ? "flex-row-reverse" : ""}`}>
              
              {/* Avatar */}
              <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${msg.role === "user" ? "bg-black text-white" : "bg-gray-100 text-black border border-gray-200"}`}>
                {msg.role === "user" ? <User size={20} /> : <Bot size={20} />}
              </div>

              {/* Message Bubble */}
              <div className={`flex flex-col gap-1 max-w-[80%] ${msg.role === "user" ? "items-end" : "items-start"}`}>
                <div className={`px-5 py-3 rounded-2xl whitespace-pre-wrap ${msg.role === "user" ? "bg-black text-white rounded-tr-none" : "bg-white text-black border border-gray-200 rounded-tl-none shadow-sm " + (msg.content === '' ? 'hidden' : '')}`}>
                  <span>{msg.content}</span>
                </div>

                {/* Accuracy & SQL Badges (Only for AI) */}
                {msg.role === "ai" && index > 0 && (
                  <div className="flex flex-wrap gap-2 mt-1">
                    {msg.isClarification && (
                      <span className="inline-flex items-center gap-1 text-xs font-medium px-2 py-1 bg-amber-50 text-amber-700 border border-amber-200 rounded-md">
                        <AlertCircle size={12} /> Clarification Needed
                      </span>
                    )}
                    {msg.sql && (
                      <span className="inline-flex items-center gap-1 text-xs font-medium px-2 py-1 bg-blue-50 text-blue-700 border border-blue-200 rounded-md font-mono">
                        <Database size={12} /> SQL Generated
                      </span>
                    )}
                    {msg.accuracyScore !== null && msg.accuracyScore !== undefined && (
                      <span className="inline-flex items-center gap-1 text-xs font-medium px-2 py-1 bg-green-50 text-green-700 border border-green-200 rounded-md">
                        <CheckCircle2 size={12} /> Confidence: {msg.accuracyScore}%
                      </span>
                    )}
                  </div>
                )}
              </div>

            </div>
          ))}

          {/* Loading Indicator (Only shown before first token arrives) */}
          {isLoading && (
            <div className="flex gap-4">
              <div className="w-10 h-10 rounded-full flex items-center justify-center bg-gray-100 text-black border border-gray-200">
                <Bot size={20} />
              </div>
              <div className="px-5 py-4 rounded-2xl bg-white border border-gray-200 rounded-tl-none shadow-sm flex items-center gap-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input Area */}
      <footer className="p-4 border-t border-gray-200 bg-white">
        <div className="max-w-3xl mx-auto relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Ask a question about the database..."
            className="w-full px-5 py-4 pr-12 rounded-full border border-gray-300 focus:outline-none focus:border-black focus:ring-1 focus:ring-black transition-all bg-gray-50 hover:bg-white"
            disabled={isLoading}
          />
          <button 
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="absolute right-2 top-2 bottom-2 aspect-square rounded-full bg-black text-white flex items-center justify-center hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Send size={18} />
          </button>
        </div>
      </footer>
    </div>
  );
}
