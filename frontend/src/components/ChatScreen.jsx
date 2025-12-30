import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import Message from '@/components/Message';
import TypingIndicator from '@/components/TypingIndicator';

/**
 * IMPORTANT:
 * This must point to your Railway backend
 * which is already mapped to your custom domain
 */
const API_URL = "https://ai.theleadsconnterprises.com/api/chat/predict";

const ChatScreen = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage.content
        }),
      });

      if (!response.ok) {
        throw new Error("API Error");
      }

      const data = await response.json();

      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: data.reply || "Prediction generated successfully.",
        timestamp: new Date()
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      setMessages(prev => [
        ...prev,
        {
          id: Date.now() + 2,
          type: 'ai',
          content: "⚠️ Server error. Please try again.",
          timestamp: new Date()
        }
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex-1 flex flex-col relative">
      {/* Header */}
      <header className="bg-[#1A1D24] border-b border-gray-800 px-6 py-4">
        <div className="flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-[#F57C00]" />
          <h1 className="text-lg font-semibold">TLC Predict Engine</h1>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-8">
        {messages.length === 0 ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col items-center justify-center h-full text-center"
          >
            <div className="w-20 h-20 rounded-full bg-gradient-to-br from-[#F57C00] to-[#2BB0E6] flex items-center justify-center mb-6">
              <Sparkles className="w-10 h-10 text-white" />
            </div>
            <h2 className="text-3xl font-bold mb-4 bg-gradient-to-r from-[#F57C00] to-[#2BB0E6] bg-clip-text text-transparent">
              Heyy Arshad & Ashaz 👋
            </h2>
            <p className="text-xl text-gray-300">
              I'm your personal predictor. Let's predict together.
            </p>
          </motion.div>
        ) : (
          <div className="max-w-4xl mx-auto space-y-6">
            <AnimatePresence>
              {messages.map(msg => (
                <Message key={msg.id} message={msg} />
              ))}
            </AnimatePresence>
            {isTyping && <TypingIndicator />}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input */}
      <div className="bg-[#1A1D24] border-t border-gray-800 px-6 py-4">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center gap-3 bg-[#252931] rounded-2xl px-4 py-3 border border-gray-700 focus-within:border-[#F57C00] transition">
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask anything..."
              className="flex-1 bg-transparent outline-none text-white placeholder:text-gray-500"
            />
            <Button
              onClick={handleSendMessage}
              disabled={!inputValue.trim()}
              className="bg-gradient-to-r from-[#F57C00] to-[#2BB0E6] hover:opacity-90"
            >
              <Send className="w-5 h-5" />
            </Button>
          </div>
          <p className="text-xs text-gray-600 text-center mt-3">
            Predictions may vary. Always validate critical decisions.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatScreen;
