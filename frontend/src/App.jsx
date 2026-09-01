import React, { useState, useEffect, useRef } from 'react';
import './App.css';

/* 🌌 Interactive Particle Mesh Background (Matching Reference Image) */
function ParticleMeshBackground() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let animationFrameId;

    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const handleResize = () => {
      width = (canvas.width = window.innerWidth);
      height = (canvas.height = window.innerHeight);
    };
    window.addEventListener('resize', handleResize);

    const particles = [];
    const numParticles = Math.floor((width * height) / 12000);

    for (let i = 0; i < numParticles; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        radius: Math.random() * 2 + 1,
        alpha: Math.random() * 0.5 + 0.3
      });
    }

    const render = () => {
      ctx.clearRect(0, 0, width, height);

      // Radial spotlight glow in upper center
      const gradient = ctx.createRadialGradient(width / 2, height / 3, 0, width / 2, height / 3, width * 0.5);
      gradient.addColorStop(0, 'rgba(255, 255, 255, 0.04)');
      gradient.addColorStop(0.5, 'rgba(0, 229, 255, 0.015)');
      gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, width, height);

      // Render connected particles
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0 || p.x > width) p.vx *= -1;
        if (p.y < 0 || p.y > height) p.vy *= -1;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${p.alpha})`;
        ctx.fill();

        for (let j = i + 1; j < particles.length; j++) {
          const p2 = particles[j];
          const dx = p.x - p2.x;
          const dy = p.y - p2.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 120) {
            const lineAlpha = (1 - dist / 120) * 0.25;
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = `rgba(255, 255, 255, ${lineAlpha})`;
            ctx.lineWidth = 0.8;
            ctx.stroke();
          }
        }
      }

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        pointerEvents: 'none',
        zIndex: 0
      }}
    />
  );
}

const DEFAULT_ENGINEERS = [
  { id: 'eng_1', name: 'Alex Rivera', role: 'Senior Threat Analyst', assigned_count: 0, max_capacity: 4 },
  { id: 'eng_2', name: 'Automated AI Sentinel 01', role: 'Autonomous Response Bot', assigned_count: 0, max_capacity: 10 },
  { id: 'eng_3', name: 'Elena Rostova', role: 'Data Loss Prevention Specialist', assigned_count: 0, max_capacity: 3 },
  { id: 'eng_4', name: 'Marcus Chen', role: 'Network Security Lead', assigned_count: 0, max_capacity: 5 },
  { id: 'eng_5', name: 'Sarah Connor', role: 'Incident Responder', assigned_count: 0, max_capacity: 4 },
  { id: 'eng_6', name: 'David Kim', role: 'Forensics Specialist', assigned_count: 0, max_capacity: 3 },
  { id: 'eng_7', name: 'Rachel Zane', role: 'SOC Analyst II', assigned_count: 0, max_capacity: 4 },
  { id: 'eng_8', name: 'Victor Vance', role: 'Cloud Security Architect', assigned_count: 0, max_capacity: 3 },
  { id: 'eng_9', name: 'Samantha Reed', role: 'Malware Reverse Engineer', assigned_count: 0, max_capacity: 3 },
  { id: 'eng_10', name: 'Tariq Al-Mansoor', role: 'Infrastructure Defender', assigned_count: 0, max_capacity: 4 },
  { id: 'eng_11', name: 'Automated AI Sentinel 02', role: 'Autonomous Isolation Unit', assigned_count: 0, max_capacity: 10 },
  { id: 'eng_12', name: 'Kaitlyn Diaz', role: 'Threat Hunter Lead', assigned_count: 0, max_capacity: 4 }
];

const SAMPLE_TITLES = [
  'Suspicious Fuzzing Payload',
  'Unauthorized Credential Stuffing',
  'Exfiltration Anomaly Detected',
  'Brute-Force Auth Flooding',
  'Remote Code Execution Attempt',
  'Malware C2 Beaconing'
];

const TARGETS = [
  { name: 'customer-data-vault', importance: 'Critical', sensitivity: 'Very High' },
  { name: 'auth-server-01', importance: 'High', sensitivity: 'High' },
  { name: 'api-edge-router', importance: 'High', sensitivity: 'Medium' },
  { name: 'cloud-k8s-cluster', importance: 'High', sensitivity: 'High' },
  { name: 'employee-portal', importance: 'Medium', sensitivity: 'Medium' }
];

function App() {
  const [incidents, setIncidents] = useState([]);
  const [engineers, setEngineers] = useState(DEFAULT_ENGINEERS);
  const [activities, setActivities] = useState([]);
  const [history, setHistory] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [activeView, setActiveView] = useState('dashboard');
  const [isConnected, setIsConnected] = useState(false);
  const ws = useRef(null);
  const incCounter = useRef(2050);

  // WebSocket Connection with Fallback for Vercel/Offline mode
  useEffect(() => {
    let timer = null;

    const connect = () => {
      try {
        const host = (window.location.hostname && window.location.hostname !== '') ? window.location.hostname : '127.0.0.1';
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        ws.current = new WebSocket(`${protocol}//${host}:8000/ws`);

        ws.current.onopen = () => {
          console.log("🟢 Connected to Live Python WebSocket Backend");
          setIsConnected(true);
        };

        ws.current.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            if (data.type === 'state_update') {
              setIncidents(data.incidents || []);
              setEngineers(data.engineers || []);
              setActivities(data.activities || []);
              setHistory(data.history || []);
            }
          } catch (e) {
            console.error("Error parsing WebSocket message:", e);
          }
        };

        ws.current.onclose = () => {
          setIsConnected(false);
          timer = setTimeout(connect, 4000);
        };

        ws.current.onerror = () => {
          setIsConnected(false);
          if (ws.current) ws.current.close();
        };
      } catch (err) {
        console.warn("WebSocket connection bypassed (Standalone mode active):", err);
        setIsConnected(false);
      }
    };

    connect();

    return () => {
      if (timer) clearTimeout(timer);
      if (ws.current) ws.current.close();
    };
  }, []);

  // 🤖 In-Browser Standalone Engine (Runs in background when backend WS is offline/Vercel)
  useEffect(() => {
    if (isConnected) return; // Use real backend when connected

    const generateThreatStandalone = () => {
      const score = Math.floor(Math.random() * 70) + 30;
      const title = SAMPLE_TITLES[Math.floor(Math.random() * SAMPLE_TITLES.length)];
      const targetObj = TARGETS[Math.floor(Math.random() * TARGETS.length)];
      const now = new Date().toLocaleTimeString();
      const id = `INC-${incCounter.current++}`;
      const badge = score >= 80 ? 'CRITICAL' : score >= 55 ? 'HIGH' : 'MEDIUM';

      // Pick engineer with lowest count
      const engList = [...DEFAULT_ENGINEERS];
      const assignedEng = engList[Math.floor(Math.random() * engList.length)];

      const newInc = {
        id,
        title,
        badge,
        source_ip: `192.168.${Math.floor(Math.random()*255)}.${Math.floor(Math.random()*254)+1}`,
        target: targetObj.name,
        asset_importance: targetObj.importance,
        data_sensitivity: targetObj.sensitivity,
        affected_users: Math.floor(Math.random() * 50) + 5,
        detected_time: now,
        status: 'Active',
        priority_score: score,
        ai_confidence: `${Math.floor(Math.random() * 40) + 60}%`,
        recommendation: score >= 70 ? 'Immediate Containment Required' : 'Isolate and Monitor Host',
        assigned_engineer: assignedEng,
        task_title: `Investigate ${title.toLowerCase()}`,
        task_priority: badge,
        task_status: 'Assigned',
        timeline: [
          { time: now, text: 'New threat detected by AI engine' },
          { time: now, text: `Priority score calculated: ${score}/100` },
          { time: now, text: `Task assigned to ${assignedEng.name}` }
        ],
        effect: { before: { status: 'ACTIVE', risk_score: score, traffic: 'DETECTED' }, after: null }
      };

      setIncidents(prev => [newInc, ...prev]);

      // Lifecycle progression simulation in background
      setTimeout(() => {
        setIncidents(prev => prev.map(inc => inc.id === id ? { ...inc, task_status: 'In Progress', status: 'Investigating' } : inc));
      }, 3000);

      setTimeout(() => {
        setIncidents(prev => prev.map(inc => inc.id === id ? {
          ...inc,
          task_status: 'Completed',
          status: 'Contained',
          completed_at: new Date().toLocaleTimeString(),
          effect: { before: inc.effect.before, after: { status: 'CONTAINED', risk_score: Math.max(10, score - 65), traffic: 'BLOCKED' } }
        } : inc));
      }, 7000);

      // Auto-remove after 9 seconds & move to history
      setTimeout(() => {
        setIncidents(prev => {
          const targetInc = prev.find(inc => inc.id === id);
          if (targetInc) {
            setHistory(h => [targetInc, ...h]);
          }
          return prev.filter(inc => inc.id !== id);
        });
      }, 9500);
    };

    // Generate initial sample threat
    generateThreatStandalone();

    // Background interval generating autonomous threats
    const interval = setInterval(generateThreatStandalone, 6000);
    return () => clearInterval(interval);
  }, [isConnected]);

  // Dynamic Engineer Workload recalculation for frontend UI
  const calculatedEngineers = engineers.map(eng => {
    const count = incidents.filter(i => i.assigned_engineer?.id === eng.id).length;
    return { ...eng, assigned_count: count };
  });

  const selectedIncident = incidents.find(i => i.id === selectedId) || history.find(i => i.id === selectedId) || null;

  const handleTaskClick = (id) => {
    setSelectedId(id);
    setActiveView('task-detail');
  };

  const handleBackToDashboard = () => {
    setActiveView('dashboard');
  };

  const assignTaskManual = async (incidentId, engineerId) => {
    const eng = DEFAULT_ENGINEERS.find(e => e.id === engineerId);
    setIncidents(prev => prev.map(inc => inc.id === incidentId ? { ...inc, assigned_engineer: eng } : inc));

    if (isConnected) {
      const host = window.location.hostname || '127.0.0.1';
      try {
        await fetch(`http://${host}:8000/assign`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ incident_id: incidentId, engineer_id: engineerId })
        });
      } catch (err) {
        console.error("Error assigning task:", err);
      }
    }
  };

  const triggerGenerateAlert = async () => {
    if (isConnected) {
      const host = window.location.hostname || '127.0.0.1';
      try {
        await fetch(`http://${host}:8000/alert`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            duration: Math.floor(Math.random() * 300),
            src_bytes: Math.floor(Math.random() * 1000000),
            dst_bytes: Math.floor(Math.random() * 500000),
            failed_logins: Math.floor(Math.random() * 50),
            login_attempts: Math.floor(Math.random() * 100),
            src_pkts: Math.floor(Math.random() * 5000),
            dst_pkts: Math.floor(Math.random() * 5000),
            severity: Math.floor(Math.random() * 10) + 1,
            asset_criticality: Math.floor(Math.random() * 10) + 1,
            business_impact: Math.floor(Math.random() * 10) + 1,
            affected_users: Math.floor(Math.random() * 1000) + 1
          })
        });
      } catch (err) {
        console.error("Error triggering alert:", err);
      }
    } else {
      // Trigger standalone simulation manually
      const score = Math.floor(Math.random() * 70) + 30;
      const title = SAMPLE_TITLES[Math.floor(Math.random() * SAMPLE_TITLES.length)];
      const targetObj = TARGETS[Math.floor(Math.random() * TARGETS.length)];
      const now = new Date().toLocaleTimeString();
      const id = `INC-${incCounter.current++}`;
      const badge = score >= 80 ? 'CRITICAL' : score >= 55 ? 'HIGH' : 'MEDIUM';
      const assignedEng = DEFAULT_ENGINEERS[Math.floor(Math.random() * DEFAULT_ENGINEERS.length)];

      const newInc = {
        id,
        title,
        badge,
        source_ip: `192.168.${Math.floor(Math.random()*255)}.${Math.floor(Math.random()*254)+1}`,
        target: targetObj.name,
        asset_importance: targetObj.importance,
        data_sensitivity: targetObj.sensitivity,
        affected_users: Math.floor(Math.random() * 50) + 5,
        detected_time: now,
        status: 'Active',
        priority_score: score,
        ai_confidence: `${Math.floor(Math.random() * 40) + 60}%`,
        recommendation: score >= 70 ? 'Immediate Containment Required' : 'Isolate and Monitor Host',
        assigned_engineer: assignedEng,
        task_title: `Investigate ${title.toLowerCase()}`,
        task_priority: badge,
        task_status: 'Assigned',
        timeline: [
          { time: now, text: 'New threat detected by AI engine' },
          { time: now, text: `Priority score calculated: ${score}/100` },
          { time: now, text: `Task assigned to ${assignedEng.name}` }
        ],
        effect: { before: { status: 'ACTIVE', risk_score: score, traffic: 'DETECTED' }, after: null }
      };

      setIncidents(prev => [newInc, ...prev]);

      setTimeout(() => {
        setIncidents(prev => prev.map(inc => inc.id === id ? { ...inc, task_status: 'In Progress', status: 'Investigating' } : inc));
      }, 3000);

      setTimeout(() => {
        setIncidents(prev => prev.map(inc => inc.id === id ? {
          ...inc,
          task_status: 'Completed',
          status: 'Contained',
          completed_at: new Date().toLocaleTimeString(),
          effect: { before: inc.effect.before, after: { status: 'CONTAINED', risk_score: Math.max(10, score - 65), traffic: 'BLOCKED' } }
        } : inc));
      }, 7000);

      setTimeout(() => {
        setIncidents(prev => {
          const targetInc = prev.find(inc => inc.id === id);
          if (targetInc) {
            setHistory(h => [targetInc, ...h]);
          }
          return prev.filter(inc => inc.id !== id);
        });
      }, 9500);
    }
  };

  const clearStream = async () => {
    setIncidents([]);
    setSelectedId(null);
    setActiveView('dashboard');
    if (isConnected) {
      const host = window.location.hostname || '127.0.0.1';
      try {
        await fetch(`http://${host}:8000/incidents`, { method: 'DELETE' });
      } catch (err) {
        console.error("Error clearing stream:", err);
      }
    }
  };

  const getBadgeClass = (badge) => {
    if (badge === 'CRITICAL') return 'badge-critical';
    if (badge === 'HIGH') return 'badge-high';
    return 'badge-medium';
  };

  return (
    <div className="app-viewport">
      {/* 🌌 Animated Particle Network Backdrop */}
      <ParticleMeshBackground />

      {/* 🔝 HEADER BAR WITH VERCEL PILL NAV */}
      <header className="app-header">
        <div className="header-brand">
          <div className="logo-icon">🛡️</div>
          <div>
            <h1 className="brand-title">CYBER INCIDENT RESPONSE SYSTEM</h1>
            <div className="header-subtitle">FINDING MEANING INSIDE NOISE</div>
          </div>
        </div>

        {/* Floating Pill Navigation */}
        <div className="nav-pill-wrapper">
          <button 
            className={`nav-pill ${activeView === 'dashboard' ? 'active' : ''}`}
            onClick={handleBackToDashboard}
          >
            Dashboard
          </button>
          <button 
            className={`nav-pill ${activeView === 'history' ? 'active' : ''}`}
            onClick={() => setActiveView('history')}
          >
            History Log ({history.length})
          </button>
          <button className="nav-pill" onClick={clearStream}>
            Clear Queue
          </button>
          <button className="nav-pill primary" onClick={triggerGenerateAlert}>
            ⚡ Simulate Threat
          </button>
        </div>

        <div className="live-status-pill">
          <span className={isConnected ? "status-dot green" : "status-dot green"}></span>
          <span>{isConnected ? 'LIVE WS' : 'AUTONOMOUS RUNNING'}</span>
        </div>
      </header>

      {/* 🟢 VIEW 1: MAIN DASHBOARD (3 COLUMNS) */}
      {activeView === 'dashboard' && (
        <main className="sketch-top-grid" style={{ position: 'relative', zIndex: 1 }}>

          {/* 1️⃣ LEFT COLUMN: LIVE THREATS INCOMING */}
          <div className="card sketch-col">
            <div className="card-header-bar">
              <h2>LIVE THREATS INCOMING</h2>
              <span className="live-stream-badge">LIVE STREAM</span>
            </div>
            <p className="card-subtext">Continuous real-time threat telemetry</p>

            <div className="threat-feed-container">
              {incidents.length === 0 ? (
                <div className="empty-feed">
                  Waiting for incoming threats...<br/>
                  <span className="sub">Click "⚡ Simulate Threat" above</span>
                </div>
              ) : (
                incidents.map(inc => (
                  <div 
                    key={inc.id} 
                    className="incoming-threat-item"
                    onClick={() => handleTaskClick(inc.id)}
                  >
                    <div className="threat-item-top">
                      <span className={`badge ${getBadgeClass(inc.badge)}`}>{inc.badge}</span>
                      <span className="threat-time">{inc.detected_time}</span>
                    </div>
                    <div className="threat-item-title">{inc.title}</div>
                    <div className="threat-item-target">Target: {inc.target}</div>
                    <div className="threat-item-footer">
                      <span>Score: <strong className="mono">{inc.priority_score}/100</strong></span>
                      <span className="click-hint">Inspect Task ➔</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* 2️⃣ MIDDLE COLUMN: TASKS */}
          <div className="card sketch-col">
            <div className="card-header-bar">
              <h2>TASKS</h2>
              <span className="count-tag">{incidents.length} ACTIVE</span>
            </div>
            <p className="card-subtext">Click any task to inspect details on sub-page</p>

            <div className="task-stack-container">
              {incidents.length === 0 ? (
                <div className="empty-feed">No active response tasks in queue</div>
              ) : (
                [...incidents].sort((a, b) => b.priority_score - a.priority_score).map(inc => (
                  <div 
                    key={inc.id} 
                    className="task-row-card"
                    onClick={() => handleTaskClick(inc.id)}
                  >
                    <div className="task-row-left">
                      <span className="task-num-badge">{inc.id}</span>
                      <div>
                        <div className="task-name-text">{inc.task_title}</div>
                        <div className="task-meta-text">Assigned: {inc.assigned_engineer?.name}</div>
                      </div>
                    </div>
                    
                    <div className="task-row-right">
                      <div className="task-score-pill">
                        <span className="score-lbl">Score:</span>
                        <strong className="mono">{inc.priority_score}/100</strong>
                      </div>
                      <span className={`priority-bubble ${inc.badge === 'CRITICAL' ? 'red' : inc.badge === 'HIGH' ? 'yellow' : 'blue'}`}></span>
                      <span className="task-status-pill">{inc.task_status || 'Assigned'}</span>
                      <span className="task-arrow">➔</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* 3️⃣ RIGHT COLUMN: TASK ASSIGNED (Roster) */}
          <div className="card sketch-col">
            <div className="card-header-bar">
              <h2>SECURITY TEAM ROSTER</h2>
              <span className="count-tag">12 MEMBERS</span>
            </div>
            <p className="card-subtext">Live workload & task assignments</p>

            <div className="roster-stack-container">
              {[...calculatedEngineers].sort((a, b) => a.assigned_count - b.assigned_count).map(eng => {
                const capacityPct = Math.min(100, Math.round((eng.assigned_count / eng.max_capacity) * 100));
                return (
                  <div key={eng.id} className="engineer-roster-row">
                    <div className="eng-row-header">
                      <div className="eng-identity">
                        <div className="eng-avatar-circle">{eng.name.charAt(0)}</div>
                        <div>
                          <div className="eng-name-text">{eng.name}</div>
                          <div className="eng-role-sub">{eng.role}</div>
                        </div>
                      </div>
                      <div className="eng-count-badge">
                        <strong>{eng.assigned_count}</strong> tasks assigned
                      </div>
                    </div>

                    <div className="workload-bar-track">
                      <div 
                        className="workload-bar-fill"
                        style={{ 
                          width: `${capacityPct}%`,
                          backgroundColor: capacityPct >= 100 ? 'var(--critical)' : 'var(--accent-cyan)' 
                        }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

        </main>
      )}

      {/* 🔵 VIEW 2: DEDICATED TASK SUB-PAGE */}
      {activeView === 'task-detail' && (
        <main className="task-subpage-container" style={{ position: 'relative', zIndex: 1 }}>
          <div className="subpage-navigation">
            <button className="back-link" onClick={handleBackToDashboard}>
              ← Back to Main Dashboard
            </button>
            <span className="subpage-breadcrumb">Dashboard / Tasks / {selectedIncident?.id}</span>
          </div>

          {selectedIncident ? (
            <div className="subpage-card">
              
              {/* Header Bar */}
              <div className="subpage-header">
                <div>
                  <div className="subpage-tags">
                    <span className="subpage-id">{selectedIncident.id}</span>
                    <span className={`badge ${getBadgeClass(selectedIncident.badge)}`}>{selectedIncident.badge}</span>
                    <span className="subpage-time">Detected at {selectedIncident.detected_time}</span>
                  </div>
                  <h1 className="subpage-title">{selectedIncident.title}</h1>
                  <p className="subpage-target-line">Target Asset: <strong className="mono">{selectedIncident.target}</strong> ({selectedIncident.asset_importance} Asset Criticality)</p>
                </div>

                <div className="subpage-score-box">
                  <div className="score-label">AI PRIORITY SCORE</div>
                  <div className="score-val">{selectedIncident.priority_score}<span className="max">/100</span></div>
                  <div className="score-status">{selectedIncident.ai_confidence} AI Confidence</div>
                </div>
              </div>

              {/* Status Control Bar */}
              <div className="subpage-control-bar">
                <div className="control-item">
                  <span className="ctrl-lbl">ASSIGNED ANALYST / BOT</span>
                  <select
                    className="assign-select-large"
                    value={selectedIncident.assigned_engineer?.id || ''}
                    onChange={(e) => assignTaskManual(selectedIncident.id, e.target.value)}
                  >
                    {DEFAULT_ENGINEERS.map(e => (
                      <option key={e.id} value={e.id}>{e.name} ({e.role})</option>
                    ))}
                  </select>
                </div>

                <div className="control-item">
                  <span className="ctrl-lbl">TASK STATUS</span>
                  <span className="ctrl-val green">● {selectedIncident.task_status || 'Assigned'}</span>
                </div>

                <div className="control-item">
                  <span className="ctrl-lbl">SOURCE IP</span>
                  <span className="ctrl-val mono">{selectedIncident.source_ip}</span>
                </div>

                <div className="control-item">
                  <span className="ctrl-lbl">AFFECTED USERS</span>
                  <span className="ctrl-val">{selectedIncident.affected_users} Users</span>
                </div>
              </div>

              {/* 🔍 SECTION 1: EXPLAIN (AI Threat Explanation) */}
              <div className="subpage-section">
                <div className="section-title-bar">
                  <span className="icon">🧠</span>
                  <h2>EXPLAIN (AI Risk Score & Threat Breakdown)</h2>
                </div>

                <div className="explain-box">
                  <div className="explain-grid">
                    <div className="exp-item">
                      <span className="lbl">AI Model Confidence</span>
                      <span className="val">{selectedIncident.ai_confidence}</span>
                    </div>
                    <div className="exp-item">
                      <span className="lbl">Target Asset</span>
                      <span className="val mono">{selectedIncident.target}</span>
                    </div>
                    <div className="exp-item">
                      <span className="lbl">Data Sensitivity</span>
                      <span className="val">{selectedIncident.data_sensitivity}</span>
                    </div>
                    <div className="exp-item">
                      <span className="lbl">Recommended Action</span>
                      <span className="val highlight">{selectedIncident.recommendation}</span>
                    </div>
                  </div>

                  <div className="explain-text">
                    <strong>AI Analysis Explanation:</strong> Anomaly detection algorithm flagged suspicious packet flow and authentication patterns targeting <span className="mono">{selectedIncident.target}</span>. The risk score was computed at <strong className="mono">{selectedIncident.priority_score}/100</strong> based on asset importance and user exposure.
                  </div>
                </div>
              </div>

              {/* 📈 SECTION 2: PROGRESS → (Step-by-Step Task Progress) */}
              <div className="subpage-section">
                <div className="section-title-bar">
                  <span className="icon">📈</span>
                  <h2>PROGRESS → (Task Execution Pipeline)</h2>
                </div>

                <div className="progress-pipeline">
                  <div className={`pipe-step ${selectedIncident.task_status ? 'done' : ''}`}>
                    <span className="step-num">1</span>
                    <span>Assigned</span>
                  </div>
                  <div className="pipe-arrow">➔</div>
                  <div className={`pipe-step ${selectedIncident.task_status === 'In Progress' || selectedIncident.task_status === 'Completed' ? 'done' : ''}`}>
                    <span className="step-num">2</span>
                    <span>In Progress</span>
                  </div>
                  <div className="pipe-arrow">➔</div>
                  <div className={`pipe-step ${selectedIncident.task_status === 'Completed' ? 'done' : ''}`}>
                    <span className="step-num">3</span>
                    <span>Completed</span>
                  </div>
                </div>

                <div className="timeline-mini-log">
                  {selectedIncident.timeline?.map((item, idx) => (
                    <div key={idx} className="timeline-log-line">
                      <span className="t-time">{item.time}</span>
                      <span className="t-msg">{item.text}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* 💥 SECTION 3: IMPACT → (Before vs After Action Effect) */}
              <div className="subpage-section">
                <div className="section-title-bar">
                  <span className="icon">💥</span>
                  <h2>IMPACT → (Before vs. After Action Mitigation)</h2>
                </div>

                <div className="impact-cards-grid">
                  <div className="impact-card before">
                    <div className="card-lbl">BEFORE ACTION</div>
                    <div className="impact-val red">Status: {selectedIncident.effect?.before?.status || 'ACTIVE'}</div>
                    <div className="impact-val">Risk Score: {selectedIncident.effect?.before?.risk_score || selectedIncident.priority_score}</div>
                    <div className="impact-val red">Traffic: DETECTED</div>
                  </div>
                  <div className="impact-card after">
                    <div className="card-lbl">AFTER ACTION</div>
                    <div className="impact-val green">
                      Status: {selectedIncident.effect?.after ? selectedIncident.effect.after.status : 'CONTAINED'}
                    </div>
                    <div className="impact-val">
                      Risk Score: {selectedIncident.effect?.after ? selectedIncident.effect.after.risk_score : Math.max(10, selectedIncident.priority_score - 66)}
                    </div>
                    <div className="impact-val green">
                      Traffic: {selectedIncident.effect?.after ? selectedIncident.effect.after.traffic : 'BLOCKED'}
                    </div>
                  </div>
                </div>
              </div>

              {/* 🌐 SECTION 4: NODES DIAGRAM (Asset Reachability Box) */}
              <div className="subpage-section">
                <div className="section-title-bar">
                  <span className="icon">🌐</span>
                  <h2>NODES (Network Reachability Topology)</h2>
                </div>

                <div className="nodes-large-box">
                  <svg width="100%" height="140" viewBox="0 0 500 140" style={{ filter: 'drop-shadow(0 0 10px rgba(0,0,0,0.5))' }}>
                    {/* Connections Behind Nodes */}
                    <line x1="80" y1="70" x2="200" y2="40" stroke="rgba(255,255,255,0.15)" strokeWidth="3" />
                    <line x1="200" y1="40" x2="320" y2="70" stroke="rgba(255,255,255,0.15)" strokeWidth="3" />
                    <line x1="80" y1="70" x2="200" y2="100" stroke="rgba(255,255,255,0.15)" strokeWidth="3" />
                    <line x1="200" y1="100" x2="320" y2="70" stroke="rgba(255,255,255,0.15)" strokeWidth="3" />
                    <line x1="320" y1="70" x2="420" y2="70" stroke="rgba(255,255,255,0.15)" strokeWidth="3" />
                    
                    {/* Active Attack Path Highlight */}
                    <line x1="80" y1="70" x2="200" y2="40" stroke="#FF3366" strokeWidth="3" strokeDasharray="4 4" />
                    <line x1="200" y1="40" x2="320" y2="70" stroke="#FF3366" strokeWidth="3" strokeDasharray="4 4" />

                    {/* Nodes */}
                    <circle cx="80" cy="70" r="22" fill="rgba(0,0,0,0.8)" stroke="#FFFFFF" strokeWidth="2" />
                    <text x="80" y="74" fill="#FFFFFF" fontSize="10" fontWeight="700" textAnchor="middle">User</text>

                    <circle cx="200" cy="40" r="22" fill="rgba(0,0,0,0.8)" stroke="#FF3366" strokeWidth="2" />
                    <text x="200" y="44" fill="#FFFFFF" fontSize="10" fontWeight="700" textAnchor="middle">Edge</text>

                    <circle cx="200" cy="100" r="22" fill="rgba(0,0,0,0.8)" stroke="#3399FF" strokeWidth="2" />
                    <text x="200" y="104" fill="#FFFFFF" fontSize="10" fontWeight="700" textAnchor="middle">Auth</text>

                    <circle cx="320" cy="70" r="22" fill="rgba(0,0,0,0.8)" stroke="#00FF66" strokeWidth="2" />
                    <text x="320" y="74" fill="#FFFFFF" fontSize="10" fontWeight="700" textAnchor="middle">Gate</text>

                    <circle cx="420" cy="70" r="22" fill="rgba(0,0,0,0.8)" stroke="#FFB020" strokeWidth="2" />
                    <text x="420" y="74" fill="#FFFFFF" fontSize="10" fontWeight="700" textAnchor="middle">Vault</text>
                  </svg>
                </div>
              </div>

            </div>
          ) : (
            <div className="no-selection-msg">
              Task details loaded from record. <button className="back-link" onClick={handleBackToDashboard}>Return to Dashboard</button>
            </div>
          )}
        </main>
      )}

      {/* 📜 VIEW 3: HISTORY LOG TAB */}
      {activeView === 'history' && (
        <main className="task-subpage-container" style={{ position: 'relative', zIndex: 1 }}>
          <div className="subpage-navigation">
            <button className="back-link" onClick={handleBackToDashboard}>
              ← Back to Main Dashboard
            </button>
            <span className="subpage-breadcrumb">Dashboard / History Log</span>
          </div>

          <div className="subpage-card" style={{ padding: '28px' }}>
            <div className="subpage-header" style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '16px' }}>
              <div>
                <h1 className="subpage-title">COMPLETED TASK HISTORY</h1>
                <p className="subpage-target-line">Archive of automatically contained and resolved incident response tasks</p>
              </div>
              <div className="count-tag" style={{ fontSize: '0.85rem', padding: '6px 12px' }}>{history.length} CONTAINED</div>
            </div>

            <div className="threat-feed-container" style={{ maxHeight: '750px', paddingRight: '8px', marginTop: '20px' }}>
              {history.length === 0 ? (
                <div className="empty-feed">
                  No contained tasks in history yet.<br/>
                  <span className="sub">Tasks move to history automatically once investigation completes.</span>
                </div>
              ) : (
                history.map(inc => (
                  <div 
                    key={inc.id} 
                    className="incoming-threat-item" 
                    onClick={() => handleTaskClick(inc.id)}
                    style={{ display: 'grid', gridTemplateColumns: '1.2fr 2.5fr 1fr', gap: '20px', alignItems: 'center' }}
                  >
                    <div>
                      <div className="threat-item-top">
                        <span className={`badge ${getBadgeClass(inc.badge)}`}>{inc.badge}</span>
                        <span className="threat-time">{inc.completed_at || inc.detected_time}</span>
                      </div>
                      <div className="subpage-id" style={{ marginTop: '4px' }}>{inc.id}</div>
                    </div>

                    <div>
                      <div className="threat-item-title">{inc.title}</div>
                      <div className="threat-item-target">Target: <strong className="mono">{inc.target}</strong></div>
                      <div style={{ fontSize: '0.775rem', color: 'var(--text-muted)' }}>Assigned Specialist: <strong>{inc.assigned_engineer?.name}</strong></div>
                    </div>

                    <div style={{ textAlign: 'right' }}>
                      <div style={{ fontSize: '0.8rem', color: 'var(--success)', fontWeight: '800', letterSpacing: '0.05em', marginBottom: '4px' }}>✔ CONTAINED</div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Mitigated Risk: <strong className="mono" style={{ color: 'var(--text-main)' }}>{inc.effect?.after?.risk_score || 10}/100</strong></div>
                      <span className="click-hint" style={{ fontSize: '0.75rem', marginTop: '4px', display: 'inline-block' }}>View Audit ➔</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </main>
      )}

    </div>
  );
}

export default App;
