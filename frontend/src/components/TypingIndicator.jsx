import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles } from 'lucide-react';

const TypingIndicator = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      className="flex gap-4 justify-start"
    >
      <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#F57C00] to-[#2BB0E6] flex items-center justify-center flex-shrink-0 shadow-lg">
        <Sparkles className="w-5 h-5 text-white" />
      </div>

      <div className="bg-[#1A1D24] rounded-2xl px-5 py-4 border border-gray-800 shadow-lg">
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-400">AI is thinking</span>
          <div className="flex gap-1">
            {[0, 1, 2].map((index) => (
              <motion.span
                key={index}
                className="w-2 h-2 bg-gradient-to-r from-[#F57C00] to-[#2BB0E6] rounded-full"
                animate={{
                  scale: [1, 1.3, 1],
                  opacity: [0.5, 1, 0.5]
                }}
                transition={{
                  duration: 1,
                  repeat: Infinity,
                  delay: index * 0.2
                }}
              />
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default TypingIndicator;
