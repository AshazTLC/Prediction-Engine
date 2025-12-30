import React from 'react';
import { motion } from 'framer-motion';
import { Brain, LayoutDashboard, FileText } from 'lucide-react';
import { cn } from '@/lib/utils';

const Sidebar = () => {
  const [activeItem, setActiveItem] = React.useState('ai-predict');

  const menuItems = [
    { id: 'ai-predict', label: 'AI Predict', icon: Brain },
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'reports', label: 'Reports', icon: FileText }
  ];

  return (
    <motion.aside
      initial={{ x: -300 }}
      animate={{ x: 0 }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
      className="w-64 bg-[#1A1D24] border-r border-gray-800 flex flex-col"
    >
      {/* Logo Section */}
      <div className="p-6 border-b border-gray-800">
        <div className="flex items-center gap-3">
          <img 
            src="https://horizons-cdn.hostinger.com/3d1a155f-9323-4fc0-9bcb-7926220925cd/c6dd17b1e6bab967872d34848a40e029.jpg" 
            alt="The LeadsCon Enterprises Logo" 
            className="w-10 h-10 rounded-lg object-cover"
          />
          <div>
            <span className="text-sm font-bold text-white block leading-tight">The LeadsCon</span>
            <span className="text-xs text-gray-400">Enterprises</span>
          </div>
        </div>
      </div>

      {/* Menu Items */}
      <nav className="flex-1 p-4">
        <div className="space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeItem === item.id;
            
            return (
              <motion.button
                key={item.id}
                onClick={() => setActiveItem(item.id)}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className={cn(
                  'w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200',
                  isActive 
                    ? 'bg-gradient-to-r from-[#F57C00] to-[#2BB0E6] text-white shadow-lg' 
                    : 'text-gray-400 hover:text-white hover:bg-[#252931]'
                )}
              >
                <Icon className="w-5 h-5" />
                <span className="font-medium">{item.label}</span>
              </motion.button>
            );
          })}
        </div>
      </nav>

      {/* Bottom Section */}
      <div className="p-4 border-t border-gray-800">
        <div className="text-xs text-gray-500 text-center">
          <span className="block mb-1">TLC Predict Engine</span>
          <span>Version 1.0</span>
        </div>
      </div>
    </motion.aside>
  );
};

export default Sidebar;
