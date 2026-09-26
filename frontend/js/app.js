/* ======================================================
   TerraSeek — Frontend Application Logic
   Vanilla JS, state-machine architecture.
   ====================================================== */

const API = '/api/v1';

// --- Application State ---
const state = {
    currentView: 'start',       // start | loading | results | detail | error
    investigationId: null,
    candidates: [],
    selectedCandidate: null,
    error: null,
};

// --- DOM references ---
const panels = {
    start:   document.getElementById('state-start'),
    loading: document.getElementById('state-loading'),
    results: document.getElementById('state-results'),
    detail:  document.getElementById('state-detail'),
    error:   document.getElementById('state-error'),
};

// --- View switching ---
function showView(name) {
    state.currentView = name;
    Object.entries(panels).forEach(([key, el]) => {
        el.hidden = (key !== name);
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// --- API helpers ---
async function api(method, path, body) {
    const opts = {
        method,
        headers: { 'Content-Type': 'application/json' },
    };
    if (body) opts.body = JSON.stringify(body);

    const res = await fetch(`${API}${path}`, opts);
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }));
        throw new Error(err.detail || `HTTP ${res.status}`);
    }
    return res.json();
}

// =============================================
//  INVESTIGATION SUBMISSION
// =============================================
async function submitInvestigation(e) {
    e.preventDefault();

    const query     = document.getElementById('query-input').value.trim();
    const aoiSelect = document.getElementById('aoi-select');
    const aoiName   = aoiSelect.options[aoiSelect.selectedIndex].text;
    const aoiKey    = aoiSelect.value;
    const bboxStr   = aoiSelect.options[aoiSelect.selectedIndex].dataset.bbox;
    const dateStart = document.getElementById('date-start').value;
    const dateEnd   = document.getElementById('date-end').value;

    if (!query || !aoiKey || !dateStart || !dateEnd) return;

    const bbox = bboxStr.split(',').map(Number);

    showView('loading');

    try {
        const data = await api('POST', '/investigate', {
            query,
            aoi_name: aoiName,
            aoi_bbox: bbox,
            date_start: dateStart,
            date_end: dateEnd,
        });

        state.investigationId = data.investigation_id;
        state.candidates = data.candidates;
        renderResults(data);
        showView('results');
    } catch (err) {
        state.error = err.message;
        document.getElementById('error-detail').textContent = err.message;
        showView('error');
    }
}

// =============================================
//  RESULTS RENDERING
// =============================================
function renderResults(data) {
    // Meta
    document.getElementById('results-meta').textContent =
        `${data.candidate_count} candidate${data.candidate_count !== 1 ? 's' : ''} · ${data.aoi_name} · ${data.date_range}`;

    // No results
    document.getElementById('no-results').hidden = data.candidate_count > 0;

    // Cards
    const grid = document.getElementById('results-grid');
    grid.innerHTML = '';

    data.candidates.forEach(c => {
        const card = document.createElement('div');
        card.className = 'candidate-card';
        card.addEventListener('click', () => openCandidate(c.id));

        card.innerHTML = `
            <div class="card-top">
                <span class="card-location">${esc(c.location_name)}</span>
                <span class="card-priority priority-${c.investigation_priority}">${c.investigation_priority} priority</span>
            </div>
            <div class="card-summary">${esc(c.summary)}</div>
            <div class="card-meta">
                <span>Before: ${c.before_date}</span>
                <span>After: ${c.after_date}</span>
                <span>Score: ${c.ranking_score.toFixed(3)}</span>
            </div>
            <div class="card-evidence">${esc(c.primary_evidence)}</div>
        `;
        grid.appendChild(card);
    });
}

// =============================================
//  CANDIDATE DETAIL
// =============================================
async function openCandidate(candidateId) {
    showView('loading');

    try {
        const invParam = state.investigationId ? `?investigation_id=${state.investigationId}` : '';
        const detail = await api('GET', `/candidates/${candidateId}${invParam}`);
        state.selectedCandidate = detail;
        renderDetail(detail);
        showView('detail');
    } catch (err) {
        state.error = err.message;
        document.getElementById('error-detail').textContent = err.message;
        showView('error');
    }
}

function renderDetail(d) {
    // Header
    document.getElementById('detail-title').textContent = d.location_name;
    const priorityEl = document.getElementById('detail-priority');
    priorityEl.textContent = `${d.investigation_priority} investigation priority`;
    priorityEl.className = `detail-priority priority-${d.investigation_priority}`;

    // Before/After images
    document.getElementById('label-before').textContent = `BEFORE: ${d.before_date}`;
    document.getElementById('label-after').textContent = `AFTER: ${d.after_date}`;

    const imgBefore = document.getElementById('img-before');
    const imgAfter  = document.getElementById('img-after');
    const fallback  = document.getElementById('compare-fallback');

    imgBefore.src = d.before_image_url;
    imgAfter.src  = d.after_image_url;
    fallback.hidden = true;

    // Handle image load failures
    let loadErrors = 0;
    const onImgError = () => {
        loadErrors++;
        if (loadErrors >= 2) { fallback.hidden = false; }
    };
    imgBefore.onerror = onImgError;
    imgAfter.onerror  = onImgError;

    // Reset slider
    document.getElementById('compare-slider').value = 50;
    updateCompareSlider(50);

    // Sources
    document.getElementById('compare-sources').textContent =
        `Before: ${d.before_source} · After: ${d.after_source}`;

    // Priority signals
    renderSignals(d.priority_signals);

    // Evidence sections
    renderEvidenceList('evidence-observed', d.observed);
    renderEvidenceList('evidence-inferred', d.inferred);
    renderEvidenceList('evidence-contextual', d.contextual_evidence);

    // Limitations
    const limList = document.getElementById('evidence-limitations');
    limList.innerHTML = d.limitations.map(l => `<li>${esc(l)}</li>`).join('');

    // Timeline
    renderTimeline(d.timeline);

    // Quality checks
    renderQuality(d.quality_checks);

    // Warnings
    const warnSection = document.getElementById('warnings-section');
    const warnList    = document.getElementById('warnings-list');
    if (d.warnings && d.warnings.length > 0) {
        warnSection.hidden = false;
        warnList.innerHTML = d.warnings.map(w => `<li>${esc(w)}</li>`).join('');
    } else {
        warnSection.hidden = true;
    }

    // Decision buttons — reset
    document.querySelectorAll('.btn-decision').forEach(btn => btn.classList.remove('active'));
    document.getElementById('decision-notes').value = '';
    const statusEl = document.getElementById('decision-status');
    statusEl.hidden = true;

    // If a decision was already recorded
    if (d.analyst_decision) {
        const activeBtn = document.querySelector(`.btn-decision[data-decision="${d.analyst_decision}"]`);
        if (activeBtn) activeBtn.classList.add('active');
        if (d.analyst_notes) document.getElementById('decision-notes').value = d.analyst_notes;
        statusEl.hidden = false;
        statusEl.className = 'decision-status success';
        statusEl.textContent = `Decision recorded: ${d.analyst_decision}`;
    }

    // Header status
    document.getElementById('header-status').textContent =
        `investigation: ${d.investigation_id} · candidate: ${d.id}`;
}

function renderSignals(signals) {
    const grid = document.getElementById('signals-grid');
    const items = [
        { key: 'query_relevance',       label: 'Query Relevance',    color: 'var(--accent-cyan)' },
        { key: 'visual_change_strength', label: 'Visual Change',     color: 'var(--accent-emerald)' },
        { key: 'temporal_persistence',   label: 'Temporal Persistence', color: 'var(--accent-blue)' },
        { key: 'data_suitability',       label: 'Data Suitability',  color: 'var(--accent-violet)' },
        { key: 'contextual_relevance',   label: 'Contextual Relevance', color: 'var(--accent-cyan)' },
        { key: 'confounder_risk',        label: 'Confounder Risk',   color: 'var(--accent-amber)', invert: true },
    ];

    grid.innerHTML = items.map(({ key, label, color, invert }) => {
        const raw = signals[key] ?? 0;
        const pct = Math.round(raw * 100);
        const display = invert ? (raw <= 0.2 ? 'Low' : raw <= 0.5 ? 'Moderate' : 'High') : `${pct}%`;
        return `
            <div class="signal-item">
                <div class="signal-label">${label}</div>
                <div class="signal-bar-track">
                    <div class="signal-bar-fill" style="width:${pct}%; background:${color}"></div>
                </div>
                <div class="signal-value">${display}</div>
            </div>
        `;
    }).join('');
}

function renderEvidenceList(containerId, items) {
    const container = document.getElementById(containerId);
    if (!items || items.length === 0) {
        container.innerHTML = '<p style="color:var(--text-muted); font-size:0.85rem;">No items.</p>';
        return;
    }
    container.innerHTML = items.map(e => `
        <div class="evidence-item">
            <span class="evidence-item-label">${esc(e.label)}</span>
            <span class="evidence-item-value">${esc(e.value)}</span>
            <span class="evidence-item-strength strength-${e.signal_strength}">${e.signal_strength}</span>
        </div>
    `).join('');
}

function renderTimeline(entries) {
    const container = document.getElementById('timeline');
    container.innerHTML = entries.map(t => `
        <div class="timeline-entry">
            <span class="timeline-date">${t.date}</span>
            <span class="timeline-dot dot-${t.signal}"></span>
            <span class="timeline-observation">${esc(t.observation)}</span>
            <span class="timeline-source">${esc(t.source)}</span>
        </div>
    `).join('');
}

function renderQuality(checks) {
    const container = document.getElementById('quality-grid');
    container.innerHTML = checks.map(q => `
        <div class="quality-item">
            <span class="quality-name">${esc(q.check_name)}</span>
            <span class="quality-detail">${esc(q.detail)}</span>
            <span class="quality-status status-${q.status}">${q.status}</span>
        </div>
    `).join('');
}

// =============================================
//  BEFORE / AFTER SLIDER
// =============================================
function updateCompareSlider(pct) {
    const clip    = document.getElementById('compare-clip');
    const divider = document.getElementById('compare-divider');
    clip.style.width = `${100 - pct}%`;
    divider.style.left = `${pct}%`;
}

document.getElementById('compare-slider').addEventListener('input', e => {
    updateCompareSlider(Number(e.target.value));
});

// Also support dragging the divider directly
(function initDividerDrag() {
    const viewport = document.getElementById('compare-viewport');
    const divider  = document.getElementById('compare-divider');
    const slider   = document.getElementById('compare-slider');
    let dragging = false;

    divider.addEventListener('mousedown', () => { dragging = true; });
    divider.addEventListener('touchstart', () => { dragging = true; }, { passive: true });

    function onMove(clientX) {
        if (!dragging) return;
        const rect = viewport.getBoundingClientRect();
        let pct = ((clientX - rect.left) / rect.width) * 100;
        pct = Math.max(0, Math.min(100, pct));
        slider.value = pct;
        updateCompareSlider(pct);
    }

    window.addEventListener('mousemove', e => onMove(e.clientX));
    window.addEventListener('touchmove', e => onMove(e.touches[0].clientX), { passive: true });
    window.addEventListener('mouseup', () => { dragging = false; });
    window.addEventListener('touchend', () => { dragging = false; });
})();

// =============================================
//  ANALYST DECISION
// =============================================
document.getElementById('decision-buttons').addEventListener('click', async (e) => {
    const btn = e.target.closest('.btn-decision');
    if (!btn) return;

    const decision = btn.dataset.decision;
    const notes    = document.getElementById('decision-notes').value.trim();
    const statusEl = document.getElementById('decision-status');

    // Visual feedback
    document.querySelectorAll('.btn-decision').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    try {
        await api('POST', '/decisions', {
            investigation_id: state.investigationId || 'standalone',
            candidate_id: state.selectedCandidate.id,
            decision,
            notes: notes || null,
        });

        statusEl.hidden = false;
        statusEl.className = 'decision-status success';
        statusEl.textContent = `Decision recorded: ${decision}`;
    } catch (err) {
        statusEl.hidden = false;
        statusEl.className = 'decision-status';
        statusEl.style.color = 'var(--accent-red)';
        statusEl.textContent = `Error: ${err.message}`;
    }
});

// =============================================
//  EXPORT
// =============================================
document.getElementById('btn-export').addEventListener('click', async () => {
    const invId = state.investigationId;
    if (!invId) {
        alert('No active investigation to export.');
        return;
    }

    try {
        const data = await api('GET', `/export/${invId}`);
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url  = URL.createObjectURL(blob);
        const a    = document.createElement('a');
        a.href     = url;
        a.download = `terraseek_evidence_${invId}.json`;
        a.click();
        URL.revokeObjectURL(url);
    } catch (err) {
        alert(`Export failed: ${err.message}`);
    }
});

// =============================================
//  NAVIGATION
// =============================================
document.getElementById('investigate-form').addEventListener('submit', submitInvestigation);

document.getElementById('btn-back-start').addEventListener('click', () => {
    document.getElementById('header-status').textContent = '';
    showView('start');
});

document.getElementById('btn-back-results').addEventListener('click', () => {
    document.getElementById('header-status').textContent =
        `investigation: ${state.investigationId}`;
    showView('results');
});

document.getElementById('btn-retry').addEventListener('click', () => showView('start'));

// --- Example card click handlers ---
document.querySelectorAll('.example-card').forEach(card => {
    card.addEventListener('click', () => {
        document.getElementById('query-input').value = card.dataset.query;
        document.getElementById('aoi-select').value  = card.dataset.aoi;
        document.getElementById('date-start').value   = card.dataset.start;
        document.getElementById('date-end').value     = card.dataset.end;
    });
});

// =============================================
//  UTILITIES
// =============================================
function esc(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}
