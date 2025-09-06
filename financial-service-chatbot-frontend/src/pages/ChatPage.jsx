// Path :-  financial-service-chatbot-frontend/src/pages/ChatPage.jsx

import React, { useState, useRef, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";

import Navbar from "../components/Navbar";

import Footer from "../components/Footer";

import axios from "axios";

import { FaPaperPlane, FaSpinner, FaTrash, FaHome } from "react-icons/fa";



const ChatPage = () => {

  // Messages State
  const initialBot = { text: "Hello! I'm FinSathi AI. How can I help you with your financial questions today?", sender: 'bot' };
  const [messages , setMessages] = useState([initialBot])

  // Input State
  const [input , setInput]  = useState('');

  // Loading State
  const [isLoading , setIsLoading] = useState(false); 

  // Messages End Ref
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  // Handlers
  const handleClear = () => {
    setMessages([initialBot]);
  };
  const handleGoHome = () => {
    navigate('/');
  };



  useEffect(() =>{
        messagesEndRef.current?.scrollIntoView(
          {
            behavior : "smooth"
          }
        )
  } , [messages])

  const handleSend = async (e) => {
         
    e.preventDefault();

    if (input.trim() === '' || isLoading) return;

    const userMessage = {
      text : input ,
      sender : 'user'
    };


    setMessages(prev => [...prev , userMessage])

    setInput('');


    setIsLoading(true);


    try {
      const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:5000";
      const response = await axios.post(`${API_BASE}/chat`, { message: input });
      const botMessage = { text: response.data.response, sender: "bot" };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      setMessages(prev => [...prev, { text: "Error: Could not connect to backend.", sender: "bot" }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div  className="min-h-screen flex flex-col bg-white dark:bg-gray-950 transition-colors duration-300">

      <Navbar />
       
       <main className="flex-1 flex flex-col pt-24">

           <div className="flex-1 flex flex-col items-center w-full">
             
             <div className="w-full max-w-4xl flex-1 flex flex-col p-3 sm:p-4 lg:p-6">

                {/* Toolbar */}
                <div className="flex items-center justify-between gap-2 mb-3">
                  <div className="text-sm sm:text-base font-semibold text-gray-700 dark:text-gray-200">Chat</div>
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

                {/* Messages Area */}
                <div className="flex-1 space-y-4 overflow-y-auto p-4 bg-gray-100 dark:bg-gray-900 rounded-2xl shadow-inner">
                  {messages.map((msg, index) => (
                    <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                      <div className={`max-w-[85%] sm:max-w-lg px-4 py-3 rounded-2xl shadow whitespace-pre-line ${msg.sender === 'user' ? 'bg-blue-600 text-white' : 'bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100 border border-gray-200 dark:border-gray-700'}`}>
                        {msg.text}
                      </div>
                    </div>
                  ))}

                  {isLoading && (
                    <div className="flex justify-start">
                      <div className="max-w-lg px-4 py-3 rounded-2xl shadow bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-200 flex items-center gap-2">
                        <FaSpinner className="animate-spin" />
                        Thinking...
                      </div>
                    </div>
                  )}

                  {/* Auto-scroll anchor */}
                  <div ref={messagesEndRef} />
                </div>

                {/* Input Form */}
                <form onSubmit={handleSend} className="mt-4 sm:mt-6 flex items-center bg-gray-100 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-full p-2 shadow-lg">
                  <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask a question..."
                    className="flex-1 p-3 sm:p-4 rounded-full bg-transparent outline-none focus:ring-2 focus:ring-gray-200 dark:focus:ring-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400"
                  />
                  <button
                    type="submit"
                    disabled={isLoading || input.trim() === ''}
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
  )
}

export default ChatPage;