import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import Message from '@/components/Message';
import TypingIndicator from '@/components/TypingIndicator';

const API_URL = "https://web-production-da9bb.up.railway.app";

const ChatScreen = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
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
          prompt: userMessage.content, // 👈 matches Flask
        }),
      });

      const data = await response.json();

      setMessages(prev => [
        ...prev,
        {
          id: Date.now() + 1,
          type: 'ai',
          content: data.reply || "Prediction generated.",
        },
      ]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        {
          id: Date.now() + 2,
          type: 'ai',
          content: "⚠️ Server error. Please try again.",
        },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col relative">
      <header className="bg-[#1A1D24] border-b border-gray-800 px-6 py-4">
        <div className="flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-[#F57C00]" />
          <h1 className="text-lg font-semibold">TLC Predict Engine</h1>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto px-6 py-8">
        <div className="max-w-4xl mx-auto space-y-6">
          <AnimatePresence>
            {messages.map(msg => (
              <Message key={msg.id} message={msg} />
            ))}
          </AnimatePresence>
          {isTyping && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>
      </div>

      <div className="bg-[#1A1D24] border-t border-gray-800 px-6 py-4">
        <div className="max-w-4xl mx-auto flex gap-3">
          <input
            value={inputValue}
            onChange={e => setInputValue(e.target.value)}
            placeholder="Ask anything..."
            className="flex-1 bg-[#252931] rounded-xl px-4 text-white"
          />
          <Button
            onClick={handleSendMessage}
            className="bg-gradient-to-r from-[#F57C00] to-[#2BB0E6]"
          >
            <Send className="w-5 h-5" />
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ChatScreen;
