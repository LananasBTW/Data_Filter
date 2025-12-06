<script setup>
import { ref, onMounted } from 'vue'

// --- State ---
const availableFiles = ref([])       
const selectedFile = ref('')         
const tableData = ref([])            
const statusMsg = ref('Prêt')
const statusType = ref('neutral')

const filePreview = ref('')
const filterField = ref('')
const filterValue = ref('')
const saveFilename = ref('export_data.json')

const statsReport = ref(null)
const showStats = ref(false)

const API_URL = 'http://127.0.0.1:8000/api'

// --- API Helper ---
async function apiCall(endpoint, payload = null, method = 'POST') {
  statusMsg.value = "Traitement..."
  statusType.value = "loading"
  try {
    const options = { method, headers: { 'Content-Type': 'application/json' }}
    if (payload) options.body = JSON.stringify(payload)
    const response = await fetch(`${API_URL}/${endpoint}/`, options)
    const data = await response.json()
    if (data.status === 'error') throw new Error(data.message)
    statusMsg.value = "Succès"
    statusType.value = "success"
    return data
  } catch (e) {
    statusMsg.value = "Erreur"
    statusType.value = "error"
    console.error(e)
    return null
  }
}

// --- Actions ---
async function fetchFiles() {
  const res = await apiCall('files', null, 'GET')
  if (res && res.files) {
    availableFiles.value = res.files
    if (res.files.length > 0) { selectedFile.value = res.files[0]; getPreview() }
  }
}
async function getPreview() {
    if (!selectedFile.value) return
    filePreview.value = "Chargement..."
    const res = await apiCall('preview', { path: selectedFile.value })
    if (res) filePreview.value = res.preview
}
async function loadData() {
  if (!selectedFile.value) return
  showStats.value = false; statsReport.value = null
  const res = await apiCall('load', { path: selectedFile.value })
  if (res) { tableData.value = res.data; statusMsg.value = `${res.count} lignes chargées` }
}
async function applyFilter() {
  const res = await apiCall('filter', { field: filterField.value, value: filterValue.value })
  if (res) tableData.value = res.data
}
async function sortCol(colName) {
  const res = await apiCall('sort', { field: colName })
  if (res) tableData.value = res.data
}
async function getStats() {
  const res = await apiCall('stats', null, 'GET')
  if (res) { statsReport.value = res.report; showStats.value = true }
}
async function saveFile() {
  const res = await apiCall('save', { path: saveFilename.value })
  if (res) statusMsg.value = `Sauvegardé : ${res.path}`
}

onMounted(() => fetchFiles())
</script>

<template>
  <div class="viewer-container">
    
    <div class="top-bar">
        <div class="brand">
            <h1>Data<span class="highlight">Filter</span></h1>
        </div>
        <div class="status-pill" :class="statusType">
            <span class="dot"></span> {{ statusMsg }}
        </div>
    </div>
    
    <div class="dashboard-grid">
      
      <div class="sidebar">
        
        <div class="card control-card">
            <div class="card-header">
                <svg class="icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
                <h3>Fichier Source</h3>
            </div>
            <div class="card-body">
                <select v-model="selectedFile" @change="getPreview" class="input-normal">
                    <option v-for="f in availableFiles" :key="f" :value="f">{{ f }}</option>
                </select>
                <button @click="loadData" class="btn btn-primary full-width">
                    Charger les données
                </button>
            </div>
            <div v-if="filePreview" class="preview-mini">
                <div class="preview-label">Aperçu</div>
                <pre>{{ filePreview }}</pre>
            </div>
        </div>

        <div class="card control-card">
            <div class="card-header">
                <svg class="icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                <h3>Filtres</h3>
            </div>
            <div class="card-body">
                <input v-model="filterField" placeholder="Colonne (ex: age)" class="input-normal input-dark" />
                <input v-model="filterValue" placeholder="Valeur (ex: 25)" class="input-normal input-dark" />
                <button @click="applyFilter" class="btn btn-secondary full-width">Appliquer</button>
            </div>
        </div>

        <div class="card control-card">
            <div class="card-header">
                <svg class="icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path></svg>
                <h3>Outils</h3>
            </div>
            <div class="card-body tools-body">
                <button @click="getStats" class="btn btn-info full-width">
                    <svg class="icon-btn" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 20V10"></path><path d="M12 20V4"></path><path d="M6 20v-6"></path></svg>
                    Statistiques
                </button>
                
                <div class="divider"></div>
                
                <div class="save-group">
                    <input v-model="saveFilename" placeholder="Nom fichier" class="input-normal input-dark" />
                    <button @click="saveFile" class="btn btn-success">
                        <svg class="icon-btn-only" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></svg>
                    </button>
                </div>
            </div>
        </div>

      </div>

      <div class="main-content">
        
        <transition name="fade">
            <div v-if="showStats && statsReport" class="card stats-panel">
                <div class="card-header flex-between">
                    <h3>Rapport Statistique</h3>
                    <button class="btn-icon" @click="showStats = false">✕</button>
                </div>
                <div class="stats-grid">
                    <div v-for="(info, field) in statsReport" :key="field" class="stat-item">
                        <div class="stat-title">{{ field }}</div>
                        <div class="stat-metrics">
                            <span class="metric valid">{{ info.non_null_count }} <small>valides</small></span>
                            <span class="metric null" v-if="info.null_count > 0">{{ info.null_count }} <small>nulls</small></span>
                        </div>
                    </div>
                </div>
            </div>
        </transition>

        <div class="card table-card">
            <div v-if="tableData.length" class="table-responsive">
                <table>
                    <thead>
                        <tr>
                            <th v-for="(val, key) in tableData[0]" :key="key" @click="sortCol(key)">
                                <div class="th-content">
                                    {{ key }} <span class="sort-arrow">↕</span>
                                </div>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(row, i) in tableData" :key="i">
                            <td v-for="(val, key) in row" :key="key">
                                <span class="cell-content">
                                    {{ typeof val === 'object' ? JSON.stringify(val) : val }}
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div v-else class="empty-state">
                <div class="empty-icon">Select</div>
                <p>Sélectionnez un fichier et cliquez sur <strong>Charger</strong> pour visualiser les données.</p>
            </div>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
/* Layout Global */
.viewer-container { max-width: 1400px; margin: 0 auto; }

/* Top Bar */
.top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; padding: 0 10px; }
.brand h1 { font-size: 1.8rem; margin: 0; letter-spacing: -1px; }
.highlight { color: var(--primary); }

/* Status Pill */
.status-pill { padding: 6px 16px; border-radius: 50px; font-size: 0.85rem; font-weight: 600; display: flex; align-items: center; gap: 8px; background: #222; border: 1px solid #333; transition: all 0.3s ease; }
.dot { width: 8px; height: 8px; border-radius: 50%; background: #666; }
.status-pill.success { border-color: rgba(16, 185, 129, 0.3); color: #10b981; } .status-pill.success .dot { background: #10b981; }
.status-pill.error { border-color: rgba(239, 68, 68, 0.3); color: #ef4444; } .status-pill.error .dot { background: #ef4444; }
.status-pill.loading { color: #f59e0b; } .status-pill.loading .dot { background: #f59e0b; animation: pulse 1s infinite; }

/* Grid Layout */
.dashboard-grid { display: grid; grid-template-columns: 280px 1fr; gap: 25px; align-items: start; }
@media (max-width: 900px) { .dashboard-grid { grid-template-columns: 1fr; } }

/* Sidebar */
.sidebar { display: flex; flex-direction: column; gap: 25px; }

/* Cards */
.card { background: var(--bg-panel); border-radius: 12px; border: 1px solid var(--border); overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.2); }
.card-header { padding: 15px 20px; border-bottom: 1px solid var(--border); background: rgba(255,255,255,0.02); display: flex; align-items: center; gap: 10px; }
.card-header h3 { margin: 0; font-size: 0.95rem; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }
.card-body { padding: 20px; display: flex; flex-direction: column; gap: 15px; }
.icon { color: var(--primary); opacity: 0.9; }

/* Inputs */
.input-normal { width: 100%; padding: 10px 12px; background: var(--bg-input); border: 1px solid var(--border); border-radius: 6px; color: white; font-family: inherit; font-size: 0.9rem; transition: border-color 0.2s; box-sizing: border-box; }
.input-normal:focus { outline: none; border-color: var(--primary); }
.input-dark { background: #151515; }

/* Buttons */
.btn { border: none; padding: 10px 16px; border-radius: 6px; font-weight: 600; cursor: pointer; transition: all 0.2s; font-size: 0.9rem; display: inline-flex; justify-content: center; align-items: center; gap: 8px; }
.btn:hover { transform: translateY(-1px); filter: brightness(110%); }
.full-width { width: 100%; }

.btn-primary { background: var(--primary); color: white; box-shadow: 0 4px 12px rgba(100, 108, 255, 0.3); }
.btn-secondary { background: #333; color: white; border: 1px solid #444; }
.btn-info { background: #0ea5e9; color: white; }
.btn-success { background: #10b981; color: white; padding: 10px; }
.btn-icon { background: none; border: none; color: #666; cursor: pointer; font-size: 1.2rem; }

/* Preview */
.preview-mini { margin-top: 0; background: #000; border-top: 1px solid var(--border); padding: 15px; }
.preview-label { font-size: 0.7rem; color: #666; margin-bottom: 5px; text-transform: uppercase; }
.preview-mini pre { margin: 0; font-family: 'Fira Code', monospace; font-size: 0.75rem; color: #a5b4fc; white-space: pre-wrap; max-height: 150px; overflow-y: auto; line-height: 1.4; }

/* Tools */
.divider { height: 1px; background: var(--border); margin: 5px 0; }
.save-group { display: flex; gap: 8px; }

/* Stats & Table */
.stats-panel { margin-bottom: 25px; border-color: var(--primary); }
.flex-between { display: flex; justify-content: space-between; align-items: center; }
.stats-grid { padding: 20px; display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 15px; }
.stat-item { background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); }
.stat-title { color: var(--text-muted); font-size: 0.8rem; margin-bottom: 8px; }
.metric { font-size: 1.1rem; font-weight: 700; display: block; }
.metric.valid { color: #10b981; }
.metric.null { color: #ef4444; font-size: 0.9rem; margin-top: 4px; }

.table-card { min-height: 400px; display: flex; flex-direction: column; }
.table-responsive { overflow-x: auto; flex: 1; }
table { width: 100%; border-collapse: separate; border-spacing: 0; }
th { background: #1a1a1a; padding: 15px; text-align: left; font-weight: 600; color: var(--text-muted); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 10; cursor: pointer; user-select: none; white-space: nowrap; }
th:hover { color: white; background: #222; }
td { padding: 12px 15px; border-bottom: 1px solid #2a2a2a; color: #ddd; font-size: 0.9rem; white-space: nowrap; }
tr:hover td { background: rgba(255,255,255,0.03); }
.th-content { display: flex; justify-content: space-between; align-items: center; gap: 10px; }

/* Empty State (RETOUR A LA VERSION "SELECT") */
.empty-state { flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; color: var(--text-muted); opacity: 0.5; padding: 40px; }
.empty-icon { font-size: 4rem; margin-bottom: 20px; font-weight: 900; letter-spacing: -2px; opacity: 0.1; }

@keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>