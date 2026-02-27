import React, { useState, useEffect } from 'react';
import { 
  Shield, Search, LayoutDashboard, FileText, 
  AlertTriangle, Settings, ExternalLink, ShieldCheck, 
  Globe, Fingerprint, Lock, Database, Info, Share2, Server
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// --- HELPER COMPONENT: IDENTITY GRAPH ---
function IdentityGraph() {
  const nodes = [
    { id: 1, label: 'md-rasheed-dev', type: 'GitHub', x: -160, y: -80 },
    { id: 2, label: 'rasheed@gmail.com', type: 'Email', x: 180, y: -120 },
    { id: 3, label: '+91 98XXX XXX01', type: 'Phone', x: 200, y: 100 },
    { id: 4, label: 'u/rasheed_aiml', type: 'Reddit', x: -180, y: 120 },
  ];

  return (
    <div className="relative h-[550px] w-full bg-[#0d0d0e] rounded-3xl border border-[#27272a] overflow-hidden flex items-center justify-center shadow-inner">
      <div className="absolute inset-0 opacity-10 bg-[radial-gradient(#3b82f6_1px,transparent_1px)] [background-size:20px_20px]"></div>
      
      <motion.div 
        initial={{ scale: 0 }} animate={{ scale: 1 }}
        className="z-10 bg-blue-600 p-8 rounded-full shadow-[0_0_60px_rgba(37,99,235,0.6)] border-4 border-blue-400/50"
      >
        <Fingerprint size={48} className="text-white" />
      </motion.div>

      {nodes.map((node) => (
        <React.Fragment key={node.id}>
          <motion.div 
            initial={{ width: 0 }} animate={{ width: 220 }}
            transition={{ delay: 0.3, duration: 1 }}
            className="absolute h-[1px] bg-gradient-to-r from-blue-600 to-transparent origin-left opacity-50"
            style={{ 
              transform: `rotate(${Math.atan2(node.y, node.x)}rad)`,
              left: '50%', top: '50%'
            }}
          />
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 + node.id * 0.1 }}
            className="absolute bg-[#161618]/90 backdrop-blur-md border border-[#27272a] p-4 rounded-2xl shadow-2xl flex flex-col items-center min-w-[140px]"
            style={{ transform: `translate(${node.x}px, ${node.y}px)` }}
          >
            <div className="flex items-center gap-2 mb-2">
              <div className="h-1.5 w-1.5 rounded-full bg-blue-500"></div>
              <span className="text-[9px] font-black text-blue-500 uppercase tracking-widest">{node.type}</span>
            </div>
            <span className="text-xs font-mono font-bold">{node.label}</span>
          </motion.div>
        </React.Fragment>
      ))}
      
      <div className="absolute bottom-8 left-8 flex items-center gap-3 text-gray-500 text-[10px] uppercase font-black tracking-[0.2em]">
        <Share2 size={14} />
        Correlation Engine Status: Active Graph
      </div>
    </div>
  );
}

// --- MAIN APPLICATION ---
export default function App() {
  const [activeTab, setActiveTab] = useState('Dashboard');
  const [isScanning, setIsScanning] = useState(false);
  const [scanComplete, setScanComplete] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleScan = () => {
    setIsScanning(true);
    setScanComplete(false);
    setProgress(0);
    
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsScanning(false);
          setScanComplete(true);
          return 100;
        }
        return prev + 4;
      });
    }, 80);
  };

  return (
    <div className="flex min-h-screen bg-[#0a0a0b] text-white font-sans selection:bg-blue-500/30">
      
      {/* SIDEBAR */}
      <aside className="w-72 border-r border-[#27272a] bg-[#161618] p-8 hidden lg:flex flex-col sticky top-0 h-screen">
        <div className="flex items-center gap-3 mb-12 text-blue-500">
          <Shield size={36} strokeWidth={2.5} />
          <h1 className="text-2xl font-black tracking-tighter text-white uppercase italic">ShadowTrace</h1>
        </div>
        
        <nav className="space-y-3 flex-1">
          <NavItem icon={<LayoutDashboard size={20}/>} label="Dashboard" active={activeTab === 'Dashboard'} onClick={() => setActiveTab('Dashboard')} />
          <NavItem icon={<Search size={20}/>} label="Footprint Scan" active={activeTab === 'Footprint Scan'} onClick={() => setActiveTab('Footprint Scan')} />
          <NavItem icon={<Fingerprint size={20}/>} label="Identity Graph" active={activeTab === 'Identity Graph'} onClick={() => setActiveTab('Identity Graph')} />
          <NavItem icon={<FileText size={20}/>} label="DPDP Compliance" active={activeTab === 'DPDP Compliance'} onClick={() => setActiveTab('DPDP Compliance')} />
        </nav>

        <div className="pt-8 border-t border-[#27272a]">
          <NavItem icon={<Settings size={20}/>} label="Settings" active={activeTab === 'Settings'} onClick={() => setActiveTab('Settings')} />
        </div>
      </aside>

      {/* MAIN CONTENT */}
      <main className="flex-1 flex flex-col min-w-0 bg-[radial-gradient(circle_at_top_right,_#1e1b4b,_transparent_40%)]">
        
        <header className="h-20 border-b border-[#27272a] flex items-center justify-between px-10 bg-[#161618]/40 backdrop-blur-xl sticky top-0 z-50">
          <div className="flex items-center gap-3 text-[10px] font-black text-gray-500 uppercase tracking-[0.2em]">
            <Globe size={16} className={isScanning ? "animate-spin text-blue-500" : "text-blue-500/50"} />
            <span>Network Status: <span className="text-white">{isScanning ? 'Synchronizing Nodes...' : 'Encrypted & Online'}</span></span>
          </div>
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2 bg-blue-500/10 px-4 py-1.5 rounded-full border border-blue-500/20">
              <div className={`h-2 w-2 rounded-full ${isScanning ? 'bg-yellow-500' : 'bg-blue-500'} animate-pulse`}></div>
              <span className="text-[10px] font-bold text-blue-500 uppercase">Audit Level: 4</span>
            </div>
            <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-blue-600 to-blue-800 border border-white/10 flex items-center justify-center text-xs font-black">MR</div>
          </div>
        </header>

        <div className="p-10 overflow-y-auto max-w-7xl mx-auto w-full">
          
          <AnimatePresence mode="wait">
            {/* VIEW: DASHBOARD */}
            {activeTab === 'Dashboard' && (
              <motion.div key="dash" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}>
                <div className="flex flex-col xl:flex-row xl:items-center justify-between gap-8 mb-12">
                  <div>
                    <h2 className="text-4xl font-black tracking-tight mb-2">Digital Footprint Intelligence</h2>
                    <p className="text-gray-400 text-sm font-medium italic">Aggregate & Correlate Identifiers — Problem Statement #64</p>
                  </div>
                  
                  <div className="relative group w-full xl:w-[500px]">
                    <input 
                      type="text" 
                      placeholder="Target Email, Username, or UID..." 
                      className="w-full bg-[#161618] border border-[#27272a] p-5 pl-14 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500/40 transition-all text-sm shadow-inner"
                    />
                    <Search className="absolute left-4 top-5 text-gray-500" size={22} />
                    <button 
                      onClick={handleScan}
                      disabled={isScanning}
                      className="absolute right-3 top-2.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-black py-3 px-6 rounded-xl transition-all active:scale-95 disabled:bg-gray-800 disabled:text-gray-500"
                    >
                      {isScanning ? 'ANALYZING...' : 'RUN ANALYSIS'}
                    </button>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
                  <StatCard label="Discovered Points" value={scanComplete ? "1,284" : "0"} icon={<Database size={24}/>} />
                  <StatCard label="Privacy Risk" value={scanComplete ? "High (84%)" : "Ready"} progress={isScanning ? progress : (scanComplete ? 84 : 0)} color="text-blue-500" icon={<Shield size={24}/>} />
                  <StatCard label="Critical Leaks" value={scanComplete ? "12 Findings" : "0"} color="text-red-500" icon={<AlertTriangle size={24}/>} />
                </div>

                <div className="bg-[#161618] border border-[#27272a] rounded-[2.5rem] overflow-hidden shadow-2xl">
                  <div className="p-8 border-b border-[#27272a] bg-white/[0.02] flex justify-between items-center">
                    <h3 className="font-black uppercase tracking-widest text-xs flex items-center gap-3">
                      <Lock size={18} className="text-blue-500" />
                      Sensitive Discovery Report
                    </h3>
                  </div>
                  <div className="overflow-x-auto min-h-[400px]">
                    <table className="w-full text-left">
                      <thead className="text-[10px] uppercase font-black tracking-[0.2em] text-gray-500 bg-white/[0.01]">
                        <tr>
                          <th className="px-8 py-6">Source Node</th>
                          <th className="px-8 py-6">Match</th>
                          <th className="px-8 py-6">Data Category</th>
                          <th className="px-8 py-6">Risk</th>
                          <th className="px-8 py-6 text-right">Trace</th>
                        </tr>
                      </thead>
                      <tbody className="text-sm divide-y divide-[#27272a]">
                        {scanComplete ? (
                          <>
                            <TableRow platform="GitHub" match="rasheed-aiml" pii="Private Key" risk="Critical" />
                            <TableRow platform="Pastebin" match="mdrasheed@iar.ac.in" pii="Aadhaar ID" risk="High" />
                            <TableRow platform="Reddit" match="u/rasheed_dev" pii="Location" risk="Medium" />
                            <TableRow platform="ForumDump" match="+91 98XXX XXX01" pii="Credentials" risk="Critical" />
                          </>
                        ) : (
                          <tr><td colSpan="5" className="py-32 text-center text-gray-700 font-mono text-xs tracking-widest uppercase animate-pulse">{isScanning ? '>> BUFFERING OSINT STREAMS...' : '>> AWAITING TARGET INPUT'}</td></tr>
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>
              </motion.div>
            )}

            {/* VIEW: FOOTPRINT SCAN */}
            {activeTab === 'Footprint Scan' && (
              <motion.div key="scan" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="max-w-4xl mx-auto py-10 text-center">
                <div className="inline-block p-6 bg-blue-500/10 rounded-full mb-6 text-blue-500">
                  <Search size={48} />
                </div>
                <h2 className="text-4xl font-black mb-4 tracking-tight">Target Discovery Engine</h2>
                <p className="text-gray-400 mb-12 italic">Initiate automated aggregation across global OSINT nodes.</p>
                <div className="bg-[#161618] border border-[#27272a] p-10 rounded-[2.5rem] shadow-2xl space-y-8">
                  <div className="text-left">
                    <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest ml-1">Input Target Identifier</label>
                    <input type="text" placeholder="e.g. email@example.com, @username, or +91..." className="w-full bg-black/40 border border-[#27272a] p-5 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500 transition-all mt-2" />
                  </div>
                  <button onClick={handleScan} disabled={isScanning} className="w-full bg-blue-600 hover:bg-blue-500 py-5 rounded-2xl font-black uppercase tracking-widest transition-all shadow-lg shadow-blue-500/20 disabled:bg-gray-800 disabled:text-gray-600">
                    {isScanning ? 'Syncing OSINT Nodes...' : 'Initiate Deep Trace'}
                  </button>
                </div>
              </motion.div>
            )}

            {/* VIEW: IDENTITY GRAPH */}
            {activeTab === 'Identity Graph' && (
              <motion.div key="graph" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
                <div className="mb-10">
                  <h2 className="text-4xl font-black tracking-tight mb-2">Identifier Correlation Graph</h2>
                  <p className="text-gray-400 text-sm font-medium italic">Visualizing unified profile clustering</p>
                </div>
                <IdentityGraph />
              </motion.div>
            )}

            {/* VIEW: COMPLIANCE */}
            {activeTab === 'DPDP Compliance' && (
              <motion.div key="comp" initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 1.05 }}>
                <div className="mb-10">
                  <h2 className="text-4xl font-black tracking-tight mb-2">DPDP Audit Framework</h2>
                  <p className="text-gray-400 text-sm font-medium italic">Legal Mapping to Digital Personal Data Protection Act (2023)</p>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <ComplianceCard section="Section 8(5)" rule="Data Security Safeguards" status="Failing" desc="Unauthorized exposure of PII on 3rd party forums." />
                  <ComplianceCard section="Section 6" rule="Consent Notice" status="Violation" desc="Data processing without explicit purpose limitation." />
                  <ComplianceCard section="Section 12" rule="Right to Erasure" status="Ready" desc="Automated removal request templates available." />
                  <ComplianceCard section="Section 13" rule="Grievance Redressal" status="Verified" desc="Data Principal communication channel established." />
                </div>
              </motion.div>
            )}

            {/* VIEW: SETTINGS */}
            {activeTab === 'Settings' && (
              <motion.div key="settings" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="max-w-2xl">
                <div className="mb-10">
                  <h2 className="text-4xl font-black tracking-tight mb-2">System Configuration</h2>
                  <p className="text-gray-400 text-sm font-medium italic">Manage API keys and OSINT node connectivity.</p>
                </div>
                <div className="space-y-8">
                  <section>
                    <h3 className="text-xs font-black text-blue-500 uppercase tracking-widest mb-4 flex items-center gap-2"><Server size={14}/> Node Connectivity</h3>
                    <div className="grid gap-4">
                      <SettingsInput label="GitHub Personal Access Token" placeholder="ghp_********" />
                      <SettingsInput label="Reddit API Client ID" placeholder="client_********" />
                      <SettingsInput label="Breach Directory API" placeholder="bd_********" />
                    </div>
                  </section>
                  <section className="pt-8 border-t border-[#27272a]">
                    <h3 className="text-xs font-black text-blue-500 uppercase tracking-widest mb-4 flex items-center gap-2"><Lock size={14}/> Privacy & Logs</h3>
                    <div className="flex items-center justify-between p-5 bg-[#161618] border border-[#27272a] rounded-2xl">
                      <span className="text-sm font-bold">Auto-generate DPDP Notices</span>
                      <div className="w-12 h-6 bg-blue-600 rounded-full relative shadow-inner"><div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full"></div></div>
                    </div>
                  </section>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}

// --- UI COMPONENTS ---
function NavItem({ icon, label, active, onClick }) {
  return (
    <button onClick={onClick} className={`w-full flex items-center gap-4 px-5 py-4 rounded-2xl transition-all duration-300 ${active ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/20 translate-x-1' : 'text-gray-500 hover:text-white hover:bg-white/5'}`}>
      <span className={active ? "text-white" : "text-gray-500 group-hover:text-white"}>{icon}</span>
      <span className="font-bold text-sm tracking-wide">{label}</span>
    </button>
  );
}

function StatCard({ label, value, icon, progress, color = "text-white" }) {
  return (
    <div className="bg-[#161618] border border-[#27272a] p-8 rounded-[2rem] shadow-xl hover:border-blue-500/40 transition-all">
      <div className="flex justify-between items-start mb-6">
        <span className="text-gray-500 text-[10px] font-black uppercase tracking-[0.2em]">{label}</span>
        <div className="text-blue-500 bg-blue-500/10 p-3 rounded-xl">{icon}</div>
      </div>
      <div className={`text-4xl font-black mb-4 ${color}`}>{value}</div>
      {progress !== undefined && (
        <div className="w-full bg-gray-800 h-1.5 rounded-full overflow-hidden">
          <motion.div initial={{ width: 0 }} animate={{ width: `${progress}%` }} className="bg-blue-500 h-full" />
        </div>
      )}
    </div>
  );
}

function TableRow({ platform, match, pii, risk }) {
  const riskColor = risk === 'Critical' ? 'bg-red-500' : risk === 'High' ? 'bg-orange-500' : 'bg-blue-500';
  return (
    <tr className="hover:bg-white/[0.02] transition-colors">
      <td className="px-8 py-6 font-black text-blue-500">{platform}</td>
      <td className="px-8 py-6 font-mono text-xs text-gray-400">{match}</td>
      <td className="px-8 py-6"><span className="bg-white/5 border border-white/10 px-3 py-1 rounded-lg text-[10px] font-bold text-gray-300">{pii}</span></td>
      <td className="px-8 py-6">
        <div className="flex items-center gap-2">
          <div className={`h-2 w-2 rounded-full ${riskColor}`}></div>
          <span className="text-xs font-black uppercase">{risk}</span>
        </div>
      </td>
      <td className="px-8 py-6 text-right"><button className="text-[10px] font-black border border-[#27272a] px-4 py-2 rounded-xl hover:bg-white hover:text-black transition-all">TRACE</button></td>
    </tr>
  );
}

function ComplianceCard({ section, rule, status, desc }) {
  const color = status === 'Failing' ? 'text-red-500' : status === 'Warning' ? 'text-yellow-500' : 'text-green-500';
  return (
    <div className="bg-[#161618] border border-[#27272a] p-8 rounded-[2rem] flex flex-col justify-between group hover:border-blue-500/20 transition-all">
      <div className="mb-6">
        <div className="flex justify-between items-center mb-4">
          <span className="text-[10px] font-black text-blue-500 uppercase tracking-widest">{section}</span>
          <span className={`text-[9px] font-black uppercase px-3 py-1 rounded-full border border-white/5 bg-white/[0.02] ${color}`}>{status}</span>
        </div>
        <h4 className="text-xl font-black mb-2 tracking-tight">{rule}</h4>
        <p className="text-gray-500 text-xs font-medium leading-relaxed">{desc}</p>
      </div>
      <button className="flex items-center gap-2 text-[10px] font-black text-gray-400 group-hover:text-blue-500 transition-colors uppercase tracking-widest">
        Generate Remediation Plan <ExternalLink size={12} />
      </button>
    </div>
  );
}

function SettingsInput({ label, placeholder }) {
  return (
    <div className="bg-[#161618] border border-[#27272a] p-5 rounded-2xl">
      <p className="text-[10px] font-black text-gray-500 uppercase mb-2 tracking-widest">{label}</p>
      <input type="password" placeholder={placeholder} className="w-full bg-black/20 border border-white/5 p-3 rounded-xl text-sm font-mono text-blue-400 outline-none" />
    </div>
  );
}