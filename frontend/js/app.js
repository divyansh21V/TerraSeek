/* ======================================================
   TerraSeek — Enhanced Dashboard Logic (India Region)
   ====================================================== */

// ============================================================
//  MOCK DATA ENGINE (INDIA FOCUS)
// ============================================================
const MOCK_DATA = {
    mumbai_coastal: {
        candidates: [
            {
                id: 'TSK-MUM-001',
                location_name: 'Mumbai Coastal Road — Priyadarshini Park Reclamation',
                summary: 'Massive marine reclamation confirmed. New seawall and approx 0.8 km² of filled land detected along the western shoreline.',
                investigation_priority: 'HIGH',
                before_date: '2021-02-15',
                after_date: '2024-03-10',
                sensor: 'Sentinel-2A / Sentinel-1',
                resolution: '10m',
                cloud_pct: 1.2,
                ranking_score: 0.982,
                primary_evidence: 'Water-to-Land Transition (NDWI Inversion)',
                bbox: [18.95, 72.79, 18.97, 72.81], // Lat/Lng
                evidence: { spectral_diff: 0.95, semantic_match: 0.98, spatial_rel: 0.91, quality: 0.96 },
                timeline: [
                    { date: '2021-02-15', signal: 'baseline', obs: 'Natural coastline, shallow coastal waters', src: 'Sentinel-2' },
                    { date: '2022-05-10', signal: 'weak', obs: 'Seawall boundary construction initiated', src: 'Sentinel-2' },
                    { date: '2023-01-20', signal: 'strong', obs: 'Infill material visible, SAR backscatter spike', src: 'Sentinel-1' },
                    { date: '2024-03-10', signal: 'persistent', obs: 'Reclamation complete, road surface grading', src: 'Sentinel-2' },
                ],
                confounders: [
                    { name: 'Tidal Fluctuation', status: 'clear', detail: 'Tide-normalized. Imagery captured at Mean Sea Level (MSL).' },
                    { name: 'Cloud/Haze', status: 'clear', detail: '1.2% cloud cover. Coastal haze mitigated.' },
                    { name: 'Sensor Co-registration', status: 'low', detail: 'Offset 0.1px. Excellent alignment.' }
                ],
                confidence: { score: 98, false_pos: 1.2, spatial_err: '±10m' }
            }
        ],
        query_tags: ['Mumbai', 'Coastal Reclamation', 'Marine Infrastructure']
    },
    himalayan_dam: {
        candidates: [
            {
                id: 'TSK-HIM-002',
                location_name: 'Dibang Valley — Hydropower Dam Early Works',
                summary: 'Large-scale earthmoving, forest clearing, and access road construction detected on steep riverbank gradients.',
                investigation_priority: 'CRITICAL',
                before_date: '2022-10-05',
                after_date: '2024-04-22',
                sensor: 'Landsat-9 / Sentinel-2',
                resolution: '15m (Pan-sharpened)',
                cloud_pct: 8.5,
                ranking_score: 0.945,
                primary_evidence: 'Canopy Loss + Terrain Alteration (DEM Variance)',
                bbox: [28.25, 95.80, 28.30, 95.85],
                evidence: { spectral_diff: 0.88, semantic_match: 0.94, spatial_rel: 0.89, quality: 0.82 },
                timeline: [
                    { date: '2022-10-05', signal: 'baseline', obs: 'Intact montane broadleaf forest', src: 'Landsat-9' },
                    { date: '2023-04-12', signal: 'weak', obs: 'Access road zig-zag pattern emerging', src: 'Sentinel-2' },
                    { date: '2023-11-20', signal: 'strong', obs: 'River bank cleared, cofferdam staging', src: 'Sentinel-2' },
                    { date: '2024-04-22', signal: 'persistent', obs: 'Massive excavation scar visible (1.2 km²)', src: 'Sentinel-2' },
                ],
                confounders: [
                    { name: 'Topographic Shadow', status: 'warning', detail: 'Steep valley walls. Sun elevation 42° - partial shadow masking applied.' },
                    { name: 'Cloud/Snow Mask', status: 'clear', detail: 'Below snowline. 8.5% cloud cover outside AOI.' },
                    { name: 'Seasonal Phenology', status: 'low', detail: 'Deciduous baseline accounted for via harmonic regression.' }
                ],
                confidence: { score: 91, false_pos: 4.8, spatial_err: '±30m (Terrain)' }
            }
        ],
        query_tags: ['Arunachal Pradesh', 'Dam Construction', 'Deforestation']
    },
    sundarbans: {
        candidates: [
            {
                id: 'TSK-SUN-003',
                location_name: 'Sundarbans Reserve — Sector 4',
                summary: 'Mangrove canopy degradation and conversion to grid-like aquaculture ponds.',
                investigation_priority: 'HIGH',
                before_date: '2021-11-10',
                after_date: '2024-02-18',
                sensor: 'Sentinel-1 (SAR)',
                resolution: '10m',
                cloud_pct: 0.0, // SAR
                ranking_score: 0.892,
                primary_evidence: 'SAR Texture Change (Rough to Smooth)',
                bbox: [21.85, 88.75, 21.90, 88.80],
                evidence: { spectral_diff: 0.92, semantic_match: 0.85, spatial_rel: 0.80, quality: 0.99 },
                timeline: [
                    { date: '2021-11-10', signal: 'baseline', obs: 'High volumetric backscatter (dense canopy)', src: 'Sentinel-1' },
                    { date: '2022-08-15', signal: 'weak', obs: 'Scattered canopy loss detected', src: 'Sentinel-1' },
                    { date: '2023-06-10', signal: 'strong', obs: 'Grid structures forming (bunds)', src: 'Sentinel-1' },
                    { date: '2024-02-18', signal: 'persistent', obs: 'Complete conversion to specular reflection (water)', src: 'Sentinel-1' },
                ],
                confounders: [
                    { name: 'Tidal Inundation', status: 'warning', detail: 'High tide can mimic canopy loss in SAR. Cross-referenced with optical.' },
                    { name: 'Speckle Noise', status: 'clear', detail: 'Lee filter applied (5x5). Signal-to-noise ratio nominal.' }
                ],
                confidence: { score: 88, false_pos: 6.2, spatial_err: '±15m' }
            }
        ],
        query_tags: ['Sundarbans', 'Mangrove Loss', 'Aquaculture']
    },
    punjab_agri: {
        candidates: [
            {
                id: 'TSK-PUN-004',
                location_name: 'Ludhiana District — Post-Harvest Burning',
                summary: 'Widespread thermal anomalies and burn scars detected over a 3-week period post-Kharif harvest.',
                investigation_priority: 'MODERATE',
                before_date: '2023-10-15',
                after_date: '2023-11-10',
                sensor: 'VIIRS / Sentinel-2',
                resolution: '375m / 10m',
                cloud_pct: 2.1,
                ranking_score: 0.975,
                primary_evidence: 'Active Fire Detections (FRP) + NBR Drop',
                bbox: [30.80, 75.75, 30.95, 75.95],
                evidence: { spectral_diff: 0.98, semantic_match: 0.95, spatial_rel: 0.88, quality: 0.94 },
                timeline: [
                    { date: '2023-10-15', signal: 'baseline', obs: 'High NDVI (Mature crops)', src: 'Sentinel-2' },
                    { date: '2023-10-25', signal: 'weak', obs: 'Harvesting visible, NDVI drops', src: 'Sentinel-2' },
                    { date: '2023-11-02', signal: 'strong', obs: 'Multiple thermal anomalies (FRP > 15MW)', src: 'VIIRS' },
                    { date: '2023-11-10', signal: 'persistent', obs: 'Large blackened burn scars visible', src: 'Sentinel-2' },
                ],
                confounders: [
                    { name: 'Urban Heat Islands', status: 'clear', detail: 'Masked out known industrial/urban thermal sources.' },
                    { name: 'Cloud/Smoke Obscuration', status: 'warning', detail: 'Heavy smoke plume partially masks optical burn scars.' }
                ],
                confidence: { score: 99, false_pos: 0.5, spatial_err: '±375m (Thermal)' }
            }
        ],
        query_tags: ['Punjab', 'Crop Fires', 'Thermal Anomaly']
    }
};

// ============================================================
//  STATE
// ============================================================
const appState = {
    currentScreen: 'landing',
    selectedAOI: null,
    query: '',
    candidates: [],
    selectedCandidate: null,
    decision: null,
    notes: ''
};

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);
const esc = (str) => { const div = document.createElement('div'); div.textContent = str; return div.innerHTML; };

// ============================================================
//  NAVIGATION & TOASTS
// ============================================================
function showScreen(name) {
    $$('.screen').forEach(s => s.classList.remove('active'));
    $(`#screen-${name}`)?.classList.add('active');

    $$('.crumb').forEach(c => {
        if (c.dataset.target === name) {
            c.classList.add('active');
            c.classList.remove('disabled');
        } else {
            c.classList.remove('active');
        }
    });
    
    // Enable crumbs up to the current
    let found = false;
    $$('.crumb').forEach(c => {
        if (!found) c.classList.remove('disabled');
        if (c.dataset.target === name) found = true;
    });

    appState.currentScreen = name;
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showToast(message, type = 'info') {
    const container = $('#toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ============================================================
//  SCREEN 1: LANDING
// ============================================================
function initLanding() {
    // Dynamic Query Parsing
    $('#query-input').addEventListener('input', (e) => {
        updateParsedChips(e.target.value);
    });

    // Cloud Slider
    $('#cloud-threshold').addEventListener('input', (e) => {
        $('#cloud-val').textContent = `${e.target.value}%`;
    });

    // Suggestions
    $$('.suggestion-card').forEach(card => {
        card.addEventListener('click', () => {
            $('#query-input').value = card.dataset.query;
            $('#aoi-select').value = card.dataset.aoi;
            if (card.dataset.start) $('#date-start').value = card.dataset.start;
            if (card.dataset.end) $('#date-end').value = card.dataset.end;
            updateParsedChips(card.dataset.query);
            showToast('Parameters loaded. Click Execute Search.', 'info');
        });
    });

    // Form Submit
    $('#investigate-form').addEventListener('submit', (e) => {
        e.preventDefault();
        const aoi = $('#aoi-select').value;
        if (!aoi) { showToast('Please select a Target AOI', 'error'); return; }

        appState.query = $('#query-input').value;
        appState.selectedAOI = aoi;

        const data = MOCK_DATA[aoi];
        
        // Show Loading Modal
        $('#loading-overlay').hidden = false;
        $('#progress-bar').style.width = '0%';
        let step = 0;
        const steps = $$('.step-item');
        steps.forEach(s => s.classList.remove('active', 'done'));

        const iv = setInterval(() => {
            if (step > 0) {
                steps[step-1].classList.remove('active');
                steps[step-1].classList.add('done');
            }
            if (step < steps.length) {
                steps[step].classList.add('active');
                $('#progress-bar').style.width = `${((step+1)/steps.length)*100}%`;
                step++;
            } else {
                clearInterval(iv);
                setTimeout(() => {
                    $('#loading-overlay').hidden = true;
                    appState.candidates = data.candidates;
                    renderDiscovery(data);
                    showScreen('discovery');
                    setTimeout(() => { if (maplibreMap) maplibreMap.resize(); }, 300);
                    showToast('Intelligence extracted successfully.', 'success');
                }, 500);
            }
        }, 600);
    });
}

function updateParsedChips(text) {
    const container = $('#parsed-constraints');
    const lower = text.toLowerCase();
    let chips = [];
    
    if (lower.includes('reclamation') || lower.includes('marine')) chips.push('Type: Coastal Reclamation');
    if (lower.includes('dam') || lower.includes('hydro')) chips.push('Type: Infrastructure');
    if (lower.includes('fire') || lower.includes('burn')) chips.push('Type: Thermal Anomaly');
    if (lower.includes('mumbai')) chips.push('Location: Mumbai, IN');
    if (lower.includes('punjab')) chips.push('Location: Punjab, IN');
    
    container.innerHTML = chips.map(c => `<span class="p-chip">${c}</span>`).join('');
}

// ============================================================
//  SCREEN 2: DISCOVERY
// ============================================================
let maplibreMap = null;
let drawPlugin = null;

function renderDiscovery(data) {
    $('#result-count').textContent = `${data.candidates.length} candidate(s)`;
    
    const list = $('#candidate-list');
    list.innerHTML = '';

    if (!data.candidates.length) {
        list.innerHTML = `
            <div class="empty-state">
                <i class="ph ph-compass-slash" style="font-size:32px; color:var(--accent-amber)"></i>
                <h3>No credible candidates</h3>
                <p>Widen the date window or relax the quality constraints. TerraSeek will not manufacture a result.</p>
            </div>`;
        $('#discovery-map').innerHTML = '<div class="empty-map">No evidence footprint for this search</div>';
        return;
    }
    
    data.candidates.forEach((c, i) => {
        const card = document.createElement('div');
        card.className = 'c-card';
        card.style.animationDelay = `${i * 0.1}s`;
        card.innerHTML = `
            <div class="c-header">
                <div class="c-title">${esc(c.location_name)}</div>
                <div class="badge">${c.investigation_priority}</div>
            </div>
            <div style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 8px;">
                ${esc(c.summary)}
            </div>
            <div style="font-size: 0.75rem; color: var(--accent-orange); font-family: var(--font-mono)">
                Score: ${c.ranking_score.toFixed(3)}
            </div>
            <div class="c-meta">
                <span>${c.sensor}</span>
                <span>${c.resolution}</span>
                <span>☁ ${c.cloud_pct}%</span>
            </div>
        `;
        card.addEventListener('click', () => {
            $$('.c-card').forEach(x => x.classList.remove('selected'));
            card.classList.add('selected');
            appState.selectedCandidate = c;
            renderWorkbench(c);
            showScreen('workbench');
        });
        list.appendChild(card);
    });

    $$('.filter-chip').forEach(filter => {
        filter.onclick = () => {
            $$('.filter-chip').forEach(item => item.classList.remove('active'));
            filter.classList.add('active');
            const mode = filter.textContent.trim().toLowerCase();
            $$('.c-card').forEach(card => {
                const text = card.textContent.toLowerCase();
                card.hidden = mode === 'all' ? false : mode === 'high priority'
                    ? !text.includes('high') && !text.includes('critical')
                    : !text.includes(mode);
            });
        };
    });

    // Init Map
    if (maplibreMap) { maplibreMap.remove(); }
    const first = data.candidates[0];
    const center = [(first.bbox[1] + first.bbox[3]) / 2, (first.bbox[0] + first.bbox[2]) / 2];
    
    maplibreMap = new maplibregl.Map({
        container: 'discovery-map',
        style: {
            "version": 8,
            "sources": {
                "esri": {
                    "type": "raster",
                    "tiles": ["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"],
                    "tileSize": 256
                }
            },
            "layers": [{
                "id": "esri-satellite",
                "type": "raster",
                "source": "esri"
            }]
        },
        center: center,
        zoom: 11
    });

    maplibreMap.on('load', () => {
        const features = data.candidates.map(c => ({
            "type": "Feature",
            "properties": { "id": c.id },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [c.bbox[1], c.bbox[0]],
                    [c.bbox[3], c.bbox[0]],
                    [c.bbox[3], c.bbox[2]],
                    [c.bbox[1], c.bbox[2]],
                    [c.bbox[1], c.bbox[0]]
                ]]
            }
        }));

        maplibreMap.addSource('candidates', {
            "type": "geojson",
            "data": { "type": "FeatureCollection", "features": features }
        });

        maplibreMap.addLayer({
            "id": "candidates-layer",
            "type": "line",
            "source": "candidates",
            "paint": {
                "line-color": "#F43F5E",
                "line-width": 3,
                "line-dasharray": [2, 2]
            }
        });
        
        maplibreMap.addLayer({
            "id": "candidates-fill",
            "type": "fill",
            "source": "candidates",
            "paint": {
                "fill-color": "#F43F5E",
                "fill-opacity": 0.25
            }
        });

        // Init Draw Plugin
        if (typeof MapboxDraw !== 'undefined') {
            drawPlugin = new MapboxDraw({ displayControlsDefault: false });
            maplibreMap.addControl(drawPlugin);
        }
    });

    // Add map toolbar listeners
    const btnDraw = $('#map-btn-draw');
    const btnMeasure = $('#map-btn-measure');
    const btnToggle = $('#map-btn-toggle');
    
    if (btnDraw) btnDraw.onclick = () => { 
        if(drawPlugin) drawPlugin.changeMode('draw_polygon'); 
        showToast('Draw Bounding Box activated.', 'info'); 
    };
    if (btnMeasure) btnMeasure.onclick = () => { 
        if(drawPlugin) drawPlugin.changeMode('draw_line_string'); 
        showToast('Measure tool activated.', 'info'); 
    };
    if (btnToggle) btnToggle.onclick = () => showToast('Toggled Optical/SAR layers (Mock).', 'info');

    maplibreMap.on('mousemove', (e) => {
        $('#map-coords').textContent = `Lat: ${e.lngLat.lat.toFixed(4)}, Lng: ${e.lngLat.lng.toFixed(4)}`;
    });
}

// ============================================================
//  SCREEN 3: WORKBENCH (Dashboard)
// ============================================================
function renderWorkbench(c) {
    $('#wb-location-title').textContent = c.location_name;
    $('#wb-priority-badge').textContent = c.investigation_priority;
    $('#wb-before-label').textContent = `T1 Baseline: ${c.before_date}`;
    $('#wb-after-label').textContent = `T2 Obs: ${c.after_date}`;

    // 1. Evidence Decomp
    $('#decomposition-grid').innerHTML = [
        { l: 'Spectral Match', s: c.evidence.spectral_diff },
        { l: 'Semantic Context', s: c.evidence.semantic_match },
        { l: 'Spatial Alignment', s: c.evidence.spatial_rel }
    ].map(item => `
        <div class="decomp-item">
            <div class="d-label"><span>${item.l}</span><span style="color:var(--accent-orange)">${(item.s*100).toFixed(0)}%</span></div>
            <div class="d-bar"><div class="d-fill" style="width:${item.s*100}%; background:var(--accent-orange)"></div></div>
        </div>
    `).join('');

    // 2. Temporal Timeline
    $('#temporal-timeline').innerHTML = c.timeline.map(t => `
        <div class="tl-node" style="border-color: ${t.signal === 'baseline' ? 'var(--text-muted)' : 'var(--accent-orange)'}">
            <div style="font-family:var(--font-mono); font-size:0.75rem; color:var(--accent-orange)">${esc(t.date)}</div>
            <div style="font-size:0.85rem; font-weight:500; margin:4px 0">${esc(t.obs)}</div>
            <div style="font-size:0.7rem; color:var(--text-muted)">${esc(t.src)}</div>
        </div>
    `).join('');

    // 3. Change Metrics
    $('#change-analysis').innerHTML = `
        <div class="metric-box"><div class="metric-val" style="color:var(--accent-orange)">${c.evidence.spectral_diff.toFixed(2)}</div><div class="metric-lbl">Delta Variance</div></div>
        <div class="metric-box"><div class="metric-val" style="color:var(--accent-emerald)">+${(c.ranking_score * 12).toFixed(1)}%</div><div class="metric-lbl">Area Growth</div></div>
    `;

    // 5. Confounders
    const confounderGrid = $('#confounder-grid');
    if (confounderGrid) {
        confounderGrid.innerHTML = c.confounders.map(cf => `
            <div class="cf-item">
                <div>
                    <div style="font-weight:500">${esc(cf.name)}</div>
                    <div style="font-size:0.75rem; color:var(--text-muted)">${esc(cf.detail)}</div>
                </div>
                <div class="cf-status" style="background: ${cf.status==='clear' ? 'var(--accent-emerald-dim)' : 'var(--accent-amber-dim)'}; color: ${cf.status==='clear' ? 'var(--accent-emerald)' : 'var(--accent-amber)'}">
                    ${esc(cf.status).toUpperCase()}
                </div>
            </div>
        `).join('');
    }

    // 6. AI Confidence
    $('#ai-confidence-ring').innerHTML = `<span class="gauge-value">${c.confidence.score}%</span>`;
    $('.gauge-details').innerHTML = `
        <div class="gauge-stat">False Positive Risk: <span>${c.confidence.false_pos}%</span></div>
        <div class="gauge-stat">Spatial Certainty: <span>${c.confidence.spatial_err}</span></div>
    `;

    // Build DAG for later
    renderDAG(c);
    renderExportSummary(c);
}

// Swipe Slider Logic
function initSwipe() {
    const slider = $('#swipe-slider');
    const divider = $('#swipe-divider');
    const before = $('#swipe-before');
    const after = $('#swipe-after');
    const vp = $('#viewport-container');
    let dragging = false;

    function setPct(pct) {
        divider.style.left = `${pct}%`;
        after.style.left = `${pct}%`;
        before.style.right = `${100 - pct}%`;
    }

    slider.addEventListener('input', e => setPct(e.target.value));

    divider.addEventListener('mousedown', () => dragging = true);
    window.addEventListener('mouseup', () => dragging = false);
    window.addEventListener('mousemove', e => {
        if (!dragging) return;
        const rect = vp.getBoundingClientRect();
        let pct = ((e.clientX - rect.left) / rect.width) * 100;
        pct = Math.max(0, Math.min(100, pct));
        setPct(pct);
    });

    // View Modes
    $$('.mode-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            $$('.mode-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const mode = btn.dataset.mode;
            if (mode === 'swipe') {
                divider.hidden = false;
                slider.hidden = false;
                after.classList.remove('ai-mask');
                setPct(50);
            } else if (mode === 'side') {
                divider.hidden = true;
                slider.hidden = true;
                after.classList.remove('ai-mask');
                before.style.right = '50%';
                after.style.left = '50%';
            } else if (mode === 'overlay') {
                divider.hidden = true;
                slider.hidden = true;
                before.style.right = '0%';
                after.style.left = '0%';
                after.classList.add('ai-mask');
            }
        });
    });
}

// ============================================================
//  SCREEN 4: MODALS & EXPORT
// ============================================================
function renderDAG(c) {
    const nodes = [
        { i: '🛰️', l: 'Sensory Ingest', v: c.sensor },
        { i: '⚙️', l: 'Pre-Process', v: 'Atmospheric Cor.' },
        { i: '🧠', l: 'AI Extraction', v: 'Vision Transformer' },
        { i: '👤', l: 'Analyst Check', v: 'Pending' }
    ];
    $('#provenance-dag').innerHTML = nodes.map((n, i) => `
        <div class="dag-node" style="flex:1; display:flex; flex-direction:column; align-items:center; text-align:center; position:relative;">
            <div class="dag-icon" style="width:40px; height:40px; border-radius:50%; background:var(--bg-secondary); border:1px solid ${i===3 ? 'var(--accent-orange)' : 'var(--accent-emerald)'}; display:flex; align-items:center; justify-content:center; font-size:1.2rem; margin-bottom:8px; box-shadow:0 0 10px ${i===3 ? 'rgba(249,115,22,0.3)' : 'rgba(16,185,129,0.3)'};">
                ${n.i}
            </div>
            <div class="dag-label" style="font-size:0.75rem; font-weight:600; color:var(--text-primary); margin-bottom:4px;">${n.l}</div>
            <div class="dag-val" style="font-size:0.65rem; color:var(--text-muted); background:var(--bg-input); padding:2px 6px; border-radius:4px;">${n.v}</div>
        </div>
        ${i < nodes.length - 1 ? `<div class="dag-arrow" style="flex:0.5; height:2px; background:linear-gradient(90deg, var(--accent-emerald) 0%, ${i===2 ? 'var(--accent-orange)' : 'var(--accent-emerald)'} 100%); position:relative; top:-20px;"></div>` : ''}
    `).join('');
}

function renderExportSummary(c) {
    $('#export-summary').innerHTML = `
        <h3 style="margin-bottom:12px; font-family:var(--font-head)">Package Manifest</h3>
        <div class="summary-grid">
            <div class="summary-item"><span class="s-lbl">Target ID</span><span class="s-val">${c.id}</span></div>
            <div class="summary-item"><span class="s-lbl">Location</span><span class="s-val">${c.location_name}</span></div>
            <div class="summary-item"><span class="s-lbl">T1 Baseline</span><span class="s-val">${c.before_date}</span></div>
            <div class="summary-item"><span class="s-lbl">T2 Observation</span><span class="s-val">${c.after_date}</span></div>
            <div class="summary-item"><span class="s-lbl">Sensor Data</span><span class="s-val">${c.sensor}</span></div>
            <div class="summary-item"><span class="s-lbl">Analyst Verdict</span><span class="s-val" id="manifest-verdict" style="color:var(--accent-orange)">PENDING</span></div>
        </div>
    `;
}

function initModals() {
    $('#btn-open-decision').addEventListener('click', () => {
        $('#decision-modal').hidden = false;
    });
    $('#btn-close-modal').addEventListener('click', () => {
        $('#decision-modal').hidden = true;
    });
    $('#btn-cancel-decision').addEventListener('click', () => {
        $('#decision-modal').hidden = true;
    });

    $$('.btn-decision').forEach(btn => {
        btn.addEventListener('click', () => {
            $$('.btn-decision').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });

    $('#btn-save-decision').addEventListener('click', () => {
        const active = $('.btn-decision.active');
        if (!active) { showToast('Select a verdict first', 'error'); return; }
        
        const dec = active.dataset.dec;
        appState.decision = dec;
        appState.notes = $('#analyst-notes')?.value?.trim() || '';
        $('#manifest-verdict').textContent = dec;
        $('#manifest-verdict').style.color = 'var(--accent-emerald)';
        
        // Update DAG
        const nodes = $$('.dag-node');
        nodes[nodes.length-1].querySelector('.dag-val').textContent = dec;

        showToast(`Decision logged: ${dec}`, 'success');
        $('#decision-modal').hidden = true;
    });

    $('#btn-proceed-export').addEventListener('click', () => {
        showScreen('export');
    });

    $$('.format-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            $$('.format-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });

    $('#btn-export-download').addEventListener('click', () => {
        showToast('Packaging secure export bundle...', 'info');
        
        const formatBtn = document.querySelector('.format-btn.active');
        const format = formatBtn ? formatBtn.dataset.format : 'json';

        setTimeout(() => {
            if (format !== 'json') {
                showToast(`${format.toUpperCase()} export is not implemented yet; choose JSON Evidence Package.`, 'error');
                return;
            }
            const dataToExport = appState.selectedCandidate || { message: "No candidate selected" };
            dataToExport.analyst_decision = appState.decision;
            dataToExport.analyst_notes = appState.notes;
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(dataToExport, null, 2));
            const downloadAnchorNode = document.createElement('a');
            downloadAnchorNode.setAttribute("href", dataStr);
            downloadAnchorNode.setAttribute("download", `terraseek_evidence_package_${Date.now()}.json`);
            document.body.appendChild(downloadAnchorNode); 
            downloadAnchorNode.click();
            downloadAnchorNode.remove();
            
            showToast('Export Complete. Check your downloads.', 'success');
        }, 1500);
    });
}

// ============================================================
//  PARTICLES & INIT
// ============================================================
function initParticles() {
    const canvas = $('#particle-canvas');
    const ctx = canvas.getContext('2d');
    let particles = [];
    const count = 50;

    function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
    function create() { return { x: Math.random()*canvas.width, y: Math.random()*canvas.height, vx: (Math.random()-0.5)*0.2, vy: (Math.random()-0.5)*0.2, r: Math.random()*1.5+0.5, alpha: Math.random()*0.3+0.1 }; }
    function init() { resize(); particles = Array.from({length: count}, create); }
    
    function draw() {
        ctx.clearRect(0,0,canvas.width,canvas.height);
        particles.forEach((p, i) => {
            p.x += p.vx; p.y += p.vy;
            if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
            if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
            ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2);
            ctx.fillStyle = `rgba(249,115,22,${p.alpha})`; ctx.fill();
            for(let j=i+1; j<particles.length; j++){
                const dx = p.x - particles[j].x, dy = p.y - particles[j].y, dist = Math.sqrt(dx*dx+dy*dy);
                if(dist < 100){
                    ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = `rgba(249,115,22,${0.05*(1-dist/100)})`; ctx.stroke();
                }
            }
        });
        requestAnimationFrame(draw);
    }
    window.addEventListener('resize', resize);
    init(); draw();
}

function bootTerraSeek() {
    initParticles();
    initLanding();
    initSwipe();
    initModals();
    
    $$('.crumb').forEach(c => {
        c.addEventListener('click', () => {
            if (!c.classList.contains('disabled')) showScreen(c.dataset.target);
        });
    });
    $('#brand-home').addEventListener('click', () => showScreen('landing'));
}

// The app is loaded dynamically in the desktop prototype. If the import
// resolves after DOMContentLoaded, waiting for that event would leave every
// control inert. Support both normal script loading and dynamic module load.
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bootTerraSeek, { once: true });
} else {
    bootTerraSeek();
}
