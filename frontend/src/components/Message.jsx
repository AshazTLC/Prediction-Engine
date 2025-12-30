import React from 'react';
import { motion } from 'framer-motion';
import { User, Sparkles } from 'lucide-react';
import { cn } from '@/lib/utils';

const Message = ({ message }) => {
  const isUser = message.type === 'user';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.3 }}
      className={cn(
        'flex gap-4',
        isUser ? 'justify-end' : 'justify-start'
      )}
    >
      {!isUser && (
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.1 }}
          className="w-10 h-10 rounded-full bg-gradient-to-br from-[#F57C00] to-[#2BB0E6] flex items-center justify-center flex-shrink-0 shadow-lg"
        >
          <Sparkles className="w-5 h-5 text-white" />
        </motion.div>
      )}

      <motion.div
        whileHover={{ scale: 1.01 }}
        className={cn(
          'max-w-[70%] rounded-2xl px-5 py-4 shadow-lg',
          isUser
            ? 'bg-gradient-to-r from-[#F57C00] to-[#2BB0E6] text-white'
            : 'bg-[#1A1D24] text-gray-100 border border-gray-800'
        )}
      >
        <p className="text-sm leading-relaxed whitespace-pre-wrap break-words">
          {message.content}
        </p>
        <span className={cn(
          'text-xs mt-2 block',
          isUser ? 'text-white/70' : 'text-gray-500'
        )}>
          {new Date(message.timestamp).toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
          })}
        </span>
      </motion.div>

      {isUser && (
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.1 }}
          className="w-10 h-10 rounded-full bg-[#252931] flex items-center justify-center flex-shrink-0 border border-gray-700"
        >
          <User className="w-5 h-5 text-gray-400" />
        </motion.div>
      )}
    </motion.div>
  );
};

export default Message;
