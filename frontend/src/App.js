import React from 'react';
import { Helmet } from 'react-helmet';
import { Toaster } from '@/components/ui/toaster';
import Sidebar from '@/components/Sidebar';
import ChatScreen from '@/components/ChatScreen';

function App() {
  return (
    <>
      <Helmet>
        <title>TLC Predict Engine - AI Prediction Dashboard</title>
        <meta name="description" content="Professional AI prediction dashboard powered by The LeadsCon Enterprises. Get intelligent predictions and insights with TLC Predict Engine." />
      </Helmet>
      <div className="flex h-screen bg-[#0F1115] text-white overflow-hidden">
        <Sidebar />
        <ChatScreen />
        <Toaster />
      </div>
    </>
  );
}

export default App;
