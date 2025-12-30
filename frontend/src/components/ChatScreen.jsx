import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import Message from '@/components/Message';
import TypingIndicator from '@/components/TypingIndicator';

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

    // Simulate AI response
    setTimeout(() => {
      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: 'I\'m analyzing your query and generating predictions. This feature will provide intelligent insights based on your input. Stay tuned for more advanced predictions!',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiMessage]);
      setIsTyping(false);
    }, 2000);
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

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-6 py-8">
        {messages.length === 0 ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="flex flex-col items-center justify-center h-full text-center"
          >
            <motion.div
              animate={{ 
                scale: [1, 1.1, 1],
                rotate: [0, 5, -5, 0]
              }}
              transition={{ 
                duration: 3,
                repeat: Infinity,
                ease: "easeInOut"
              }}
              className="mb-6"
            >
              <div className="w-20 h-20 rounded-full bg-gradient-to-br from-[#F57C00] to-[#2BB0E6] flex items-center justify-center shadow-2xl">
                <Sparkles className="w-10 h-10 text-white" />
              </div>
            </motion.div>
            <h2 className="text-3xl font-bold mb-4 bg-gradient-to-r from-[#F57C00] to-[#2BB0E6] bg-clip-text text-transparent">
              Heyy Arshad & Ashaz 👋
            </h2>
            <p className="text-xl text-gray-300 max-w-2xl">
              I'm your personal predictor. Let's predict together.
            </p>
            <p className="text-sm text-gray-500 mt-4">
              Ask me anything and I'll provide intelligent predictions
            </p>
          </motion.div>
        ) : (
          <div className="max-w-4xl mx-auto space-y-6">
            <AnimatePresence mode="popLayout">
              {messages.map((message) => (
                <Message key={message.id} message={message} />
              ))}
            </AnimatePresence>
            {isTyping && <TypingIndicator />}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="bg-[#1A1D24] border-t border-gray-800 px-6 py-4">
        <div className="max-w-4xl mx-auto">
          <div className="relative flex items-center gap-3 bg-[#252931] rounded-2xl px-4 py-3 border border-gray-700 focus-within:border-[#F57C00] transition-all duration-200">
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
              className="bg-gradient-to-r from-[#F57C00] to-[#2BB0E6] hover:opacity-90 rounded-xl px-4 py-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-5 h-5" />
            </Button>
          </div>
          <p className="text-xs text-gray-600 text-center mt-3">
            TLC Predict Engine may produce inaccurate predictions. Always verify critical information.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatScreen;
