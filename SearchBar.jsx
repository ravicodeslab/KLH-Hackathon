import React from 'react';
import { Search } from 'lucide-react';

export default function SearchBar({ onScan, isScanning }) {
  return (
    <div className="relative group w-full xl:w-[500px]">
      <input type="text" placeholder="Target Email, Username, or ID..." className="w-full bg-[#161618] border border-[#27272a] p-5 pl-14 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500/40 transition-all text-sm shadow-inner" />
      <Search className="absolute left-5 top-5 text-gray-500" size={22} />
      <button onClick={onScan} disabled={isScanning} className="absolute right-3 top-2.5 bg-blue-600 hover:bg-blue-500 text-white text-[10px] font-black py-3 px-6 rounded-xl transition-all active:scale-95 disabled:bg-gray-800">
        {isScanning ? 'ANALYZING...' : 'RUN ANALYSIS'}
      </button>
    </div>
  );
}