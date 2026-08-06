import React from 'react';
import { CheckCircle2, LogOut, ShieldCheck, Users, TrendingUp, Sparkles, Building } from 'lucide-react';

export default function SuccessState({ user, onLogout }) {
  return (
    <div className="success-screen">
      <div className="success-badge">
        <CheckCircle2 size={36} />
      </div>

      <div className="user-avatar-lg">
        {user.name ? user.name.charAt(0).toUpperCase() : 'U'}
      </div>

      <h2 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.8rem', fontWeight: 800, marginBottom: '6px' }}>
        Welcome back, {user.name || 'Alex Morgan'}!
      </h2>
      <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', marginBottom: '28px' }}>
        You are securely authenticated as <strong style={{ color: 'var(--accent-primary)' }}>{user.email}</strong>
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px', marginBottom: '32px', textAlign: 'left' }}>
        <div style={{ background: 'var(--bg-input)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--accent-primary)', fontSize: '0.8rem', fontWeight: 600, marginBottom: '6px' }}>
            <Users size={14} /> ACTIVE EMPLOYEES
          </div>
          <div style={{ fontSize: '1.3rem', fontWeight: 800 }}>12,840</div>
          <div style={{ fontSize: '0.75rem', color: 'var(--accent-emerald)', marginTop: '4px' }}>↑ 4.2% this month</div>
        </div>

        <div style={{ background: 'var(--bg-input)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--accent-secondary)', fontSize: '0.8rem', fontWeight: 600, marginBottom: '6px' }}>
            <TrendingUp size={14} /> RETENTION INDEX
          </div>
          <div style={{ fontSize: '1.3rem', fontWeight: 800 }}>98.6%</div>
          <div style={{ fontSize: '0.75rem', color: 'var(--accent-emerald)', marginTop: '4px' }}>Top 5% Industry</div>
        </div>

        <div style={{ background: 'var(--bg-input)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--accent-cyan)', fontSize: '0.8rem', fontWeight: 600, marginBottom: '6px' }}>
            <Sparkles size={14} /> AI INSIGHTS
          </div>
          <div style={{ fontSize: '1.3rem', fontWeight: 800 }}>24 New</div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '4px' }}>Real-time sync</div>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '16px' }}>
        <button
          onClick={onLogout}
          className="submit-btn"
          style={{
            maxWidth: '240px',
            background: 'var(--bg-input)',
            border: '1px solid var(--border-color)',
            color: 'var(--text-primary)'
          }}
        >
          <LogOut size={18} /> Sign Out
        </button>
      </div>
    </div>
  );
}
