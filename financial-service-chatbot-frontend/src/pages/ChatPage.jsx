// Path :-  financial-service-chatbot-frontend/src/pages/ChatPage.jsx
//
// This component renders the main chat interface where users interact
// with the FinSathi AI financial chatbot.
//
// KEY FEATURES:
//   - Real-time chat UI with user/bot message bubbles
//   - Auto-scroll to latest message
//   - Loading spinner while waiting for AI response
//   - Retry button on failed messages
//   - Source link extraction and clickable rendering
//   - Clear chat and Home navigation buttons
//
// API INTEGRATION:
//   - Sends POST requests to the backend /chat endpoint
//   - Uses VITE_API_BASE env var for production URL (defaults to localhost)

import React, { useState, useRef, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";

import Navbar from "../components/Navbar";

import Footer from "../components/Footer";

import axios from "axios";

import { FaPaperPlane, FaSpinner, FaTrash, FaHome, FaRedo } from "react-icons/fa";

const ChatPage = () => {
  // ── State Management ─────────────────────────────────────────────
  // Initial bot greeting message shown when chat page loads
  const initialBot = {
    text: "Hello! I'm FinSathi AI. How can I help you with your financial questions today?",
    sender: "bot",
  };
  const [messages, setMessages] = useState([initialBot]);

  // Current text in the input field
  const [input, setInput] = useState("");

  // Whether we're waiting for a bot response
  const [isLoading, setIsLoading] = useState(false);

  // Ref for auto-scrolling to the bottom of messages
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  // ── Handlers ─────────────────────────────────────────────────────

  // Clear all messages and reset to initial greeting
  const handleClear = () => {
    setMessages([initialBot]);
  };

  // Navigate back to the landing page
  const handleGoHome = () => {
    navigate("/");
  };

  // Auto-scroll to bottom whenever messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  // ── Bot Content Renderer ─────────────────────────────────────────
  // Parses the bot's response text to:
  //   1. Extract the "Source: <URL>" line and render it as a clickable link
  //   2. Display the main content with preserved whitespace/newlines

  const renderBotContent = (text) => {
    // Extract source URL from the response (pattern: "Source: <url>")
    const sourceMatch = text.match(/Source:\s*(.+)$/im);
    const sourceUrl = sourceMatch ? sourceMatch[1].trim() : null;
    
    // Get content without source line
    const content = text.replace(/Source:\s*.+$/im, '').trim();
    
    // Single line responses (like greetings) — render as plain text
    if (!sourceUrl && content.split('\n').length === 1) {
      return <p className="whitespace-pre-line">{content}</p>;
    }
    
    // Multi-line responses — render with source link section
    return (
      <div>
        <div className="whitespace-pre-line leading-relaxed">{content}</div>
        {sourceUrl && (
          <div className="mt-4 pt-3 border-t border-gray-200 dark:border-gray-700">
            <div className="text-sm text-gray-600 dark:text-gray-400">
              <span className="font-semibold">Source:</span>{" "}
              <a
                href={sourceUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-500 hover:text-blue-600 underline break-all"
              >
                {sourceUrl}
              </a>
            </div>
          </div>
        )}
      </div>
    );
  };

  // ── Retry Handler ────────────────────────────────────────────────
  // When a message fails, the user can click "Retry" to resend
  // the last user message that triggered the error

  const handleRetry = async (originalMessage) => {
    // Remove the error message from the chat
    setMessages((prev) => prev.filter((msg) => !msg.isError));
    setIsLoading(true);

    try {
      const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:5000";
      const response = await axios.post(`${API_BASE}/chat`, { message: originalMessage });
      const botMessage = { text: response.data.response, sender: "bot" };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      // Show error with retry option
      const errorMessage = error.response?.data?.error || "Could not connect to backend. Please check if the server is running.";
      setMessages((prev) => [
        ...prev,
        {
          text: errorMessage,
          sender: "bot",
          isError: true,
          originalMessage: originalMessage,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  // ── Send Message Handler ─────────────────────────────────────────
  // Sends the user's message to the backend API and displays the response

  const handleSend = async (e) => {
    e.preventDefault();

    // Don't send empty messages or if already loading
    if (input.trim() === "" || isLoading) return;

    // Add user's message to the chat
    const userMessage = {
      text: input,
      sender: "user",
    };

    setMessages((prev) => [...prev, userMessage]);

    // Clear the input field
    const currentInput = input;
    setInput("");

    setIsLoading(true);

    try {
      // Call the backend /chat endpoint
      const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:5000";
      const response = await axios.post(`${API_BASE}/chat`, { message: currentInput });
      const botMessage = { text: response.data.response, sender: "bot" };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      // Extract the actual error message from the backend response
      // This gives users helpful info instead of a generic "connection error"
      const errorMessage = error.response?.data?.error || "Could not connect to backend. Please check if the server is running.";
      setMessages((prev) => [
        ...prev,
        {
          text: errorMessage,
          sender: "bot",
          isError: true,
          originalMessage: currentInput,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  // ── Render ───────────────────────────────────────────────────────

  return (
    <div className="min-h-screen flex flex-col bg-white dark:bg-gray-950 transition-colors duration-300">
      <Navbar />

      <main className="flex-1 flex flex-col pt-24">
        <div className="flex-1 flex flex-col items-center w-full">
          <div className="w-full max-w-4xl flex-1 flex flex-col p-3 sm:p-4 lg:p-6">
            {/* Toolbar — Clear and Home buttons */}
            <div className="flex items-center justify-between gap-2 mb-3">
              <div className="text-sm sm:text-base font-semibold text-gray-700 dark:text-gray-200">
                Chat
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={handleClear}
                  className="flex items-center gap-2 px-3 py-2 rounded-full bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200 border border-gray-200 dark:border-gray-700 transition-colors"
                >
                  <FaTrash /> <span className="hidden sm:inline">Clear</span>
                </button>
                <button
                  onClick={handleGoHome}
                  className="flex items-center gap-2 px-3 py-2 rounded-full bg-blue-600 hover:bg-blue-700 text-white transition-colors"
                >
                  <FaHome /> <span className="hidden sm:inline">Home</span>
                </button>
              </div>
            </div>

            {/* Messages Area — scrollable chat history */}
            <div className="flex-1 space-y-4 overflow-y-auto p-4 bg-gray-100 dark:bg-gray-900 rounded-2xl shadow-inner">
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`flex ${
                    msg.sender === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-[85%] sm:max-w-lg px-4 py-3 rounded-2xl shadow break-words ${
                      msg.sender === "user"
                        ? "bg-blue-600 text-white whitespace-pre-line"
                        : msg.isError
                        ? "bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-800"
                        : "bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100 border border-gray-200 dark:border-gray-700"
                    }`}
                  >
                    {/* Render message content based on type */}
                    {msg.sender === "bot" ? (
                      msg.isError ? (
                        // Error message with retry button
                        <div>
                          <p className="mb-3">⚠️ {msg.text}</p>
                          <button
                            onClick={() => handleRetry(msg.originalMessage)}
                            disabled={isLoading}
                            className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-red-100 hover:bg-red-200 dark:bg-red-800 dark:hover:bg-red-700 text-red-700 dark:text-red-200 text-sm font-medium transition-colors disabled:opacity-50"
                          >
                            <FaRedo className="text-xs" /> Retry
                          </button>
                        </div>
                      ) : (
                        renderBotContent(msg.text)
                      )
                    ) : (
                      msg.text
                    )}
                  </div>
                </div>
              ))}

              {/* Loading indicator — shown while waiting for bot response */}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="max-w-lg px-4 py-3 rounded-2xl shadow bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-200 flex items-center gap-2">
                    <FaSpinner className="animate-spin" />
                    Thinking...
                  </div>
                </div>
              )}

              {/* Auto-scroll anchor — invisible element at the bottom */}
              <div ref={messagesEndRef} />
            </div>

            {/* Input Form — message input and send button */}
            <form
              onSubmit={handleSend}
              className="mt-4 sm:mt-6 flex items-center bg-gray-100 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-full p-2 shadow-lg"
            >
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask a question..."
                className="flex-1 p-3 sm:p-4 rounded-full bg-transparent outline-none focus:ring-2 focus:ring-gray-200 dark:focus:ring-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400"
              />
              <button
                type="submit"
                disabled={isLoading || input.trim() === ""}
                className="p-2 sm:p-3 rounded-full bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 disabled:bg-gray-300 dark:disabled:bg-gray-800 disabled:cursor-not-allowed transition-colors"
              >
                <FaPaperPlane className="text-gray-600 dark:text-gray-200" />
              </button>
            </form>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default ChatPage;
