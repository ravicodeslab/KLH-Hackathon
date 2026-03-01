import React from 'react';
import { Lock } from 'lucide-react';

export default function ExposedPII({ scanComplete, isScanning }) {
  return (
    <div className="bg-[#161618] border border-[#27272a] rounded-[2.5rem] overflow-hidden shadow-2xl">
      <div className="p-8 border-b border-[#27272a] bg-white/[0.02] flex justify-between items-center">
        <h3 className="font-black uppercase tracking-widest text-xs flex items-center gap-3">
          <Lock size={18} className="text-blue-500" /> Sensitive Discovery Report
        </h3>
      </div>
      <table className="w-full text-left">
        <thead className="text-[10px] uppercase font-black text-gray-500 bg-white/[0.01]">
          <tr><th className="px-8 py-6">Source Node</th><th className="px-8 py-6">Match</th><th className="px-8 py-6">Risk</th></tr>
        </thead>
        <tbody className="text-sm divide-y divide-[#27272a]">
          {scanComplete ? (
            <tr className="hover:bg-white/[0.01]"><td className="px-8 py-6 font-black text-blue-500">GitHub</td><td className="px-8 py-6 font-mono text-xs">rasheed-aiml</td><td className="px-8 py-6 text-red-500 font-bold">Critical</td></tr>
          ) : (
            <tr><td colSpan="3" className="py-20 text-center text-gray-700 font-mono text-xs tracking-widest uppercase animate-pulse">
              {isScanning ? '>> AGGREGATING NODES...' : '>> AWAITING TARGET INPUT'}
            </td></tr>
          )}
        </tbody>
      </table>
    </div>
  );
}