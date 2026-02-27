import React from 'react';
import { Database, AlertTriangle, Fingerprint } from 'lucide-react';

export default function StatsGrid({ scanComplete }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 h-full">
      <div className="bg-[#161618] border border-[#27272a] p-8 rounded-[2rem]">
        <div className="flex justify-between items-start mb-6">
          <span className="text-gray-500 text-[10px] font-black uppercase tracking-widest">Discovered Points</span>
          <Database className="text-blue-500" size={20}/>
        </div>
        <div className="text-4xl font-black">{scanComplete ? "1,284" : "0"}</div>
      </div>
      <div className="bg-[#161618] border border-[#27272a] p-8 rounded-[2rem]">
        <div className="flex justify-between items-start mb-6">
          <span className="text-gray-500 text-[10px] font-black uppercase tracking-widest">Critical Leaks</span>
          <AlertTriangle className="text-red-500" size={20}/>
        </div>
        <div className="text-4xl font-black text-red-500">{scanComplete ? "12" : "0"}</div>
      </div>
    </div>
  );
}