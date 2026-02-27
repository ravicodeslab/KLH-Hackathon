import React from 'react';
import { Shield } from 'lucide-react';
import { motion } from 'framer-motion';

export default function RiskScoreCard({ score, isScanning, progress }) {
  const displayScore = isScanning ? progress : score;
  return (
    <div className="bg-[#161618] border border-[#27272a] p-8 rounded-[2rem] shadow-xl group hover:border-blue-500/40 transition-all h-full">
      <div className="flex justify-between items-start mb-6">
        <span className="text-gray-500 text-[10px] font-black uppercase tracking-widest">Privacy Risk Index</span>
        <div className="text-blue-500 bg-blue-500/10 p-3 rounded-xl"><Shield size={24}/></div>
      </div>
      <div className="text-5xl font-black mb-4 text-blue-500">{displayScore}%</div>
      <div className="w-full bg-gray-800 h-1.5 rounded-full overflow-hidden">
        <motion.div initial={{ width: 0 }} animate={{ width: `${displayScore}%` }} className="bg-blue-500 h-full" />
      </div>
    </div>
  );
}