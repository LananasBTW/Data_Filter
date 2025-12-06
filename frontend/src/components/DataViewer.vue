<script setup>
import { ref, onMounted } from 'vue'

const availableFiles = ref([])       
const selectedFile = ref('')         
const tableData = ref([])            
const statusMsg = ref('En attente...') 

const filterField = ref('')
const filterValue = ref('')
const saveFilename = ref('export_data.json')

const statsReport = ref(null)
const showStats = ref(false)

const API_URL = 'http://127.0.0.1:8000/api'

async function apiCall(endpoint, payload = null, method = 'POST') {
  statusMsg.value = "⏳ Traitement..."
  try {
    const options = {
      method: method,
      headers: { 'Content-Type': 'application/json' },
    }
    if (payload) options.body = JSON.stringify(payload)

    const response = await fetch(`${API_URL}/${endpoint}/`, options)
    
    if (!response.ok) {
        throw new Error(`Erreur serveur (${response.status})`)
    }

    const data = await response.json()
    if (data.status === 'error') throw new Error(data.message)
    
    statusMsg.value = "✅ Succès"
    return data
  } catch (e) {
    statusMsg.value = "❌ " + e.message
    console.error(e)
    return null
  }
}

// --- Actions ---

async function fetchFiles() {
  const res = await apiCall('files', null, 'GET')
  if (res && res.files) {
    availableFiles.value = res.files
    if (res.files.length > 0) selectedFile.value = res.files[0]
  }
}

async function loadData() {
  if (!selectedFile.value) return
  showStats.value = false
  statsReport.value = null
  const res = await apiCall('load', { path: selectedFile.value })
  if (res) {
      tableData.value = res.data
      statusMsg.value = `✅ Chargé : ${res.count} lignes.`
  }
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
  if (res) {
    statsReport.value = res.report
    showStats.value = true
  }
}

async function getPreview() {
    if (!selectedFile.value) return
    filePreview.value = "Chargement de l'aperçu..."
    
    const res = await apiCall('preview', { path: selectedFile.value })
    if (res) {
        filePreview.value = res.preview
    }
}

async function saveFile() {
  const res = await apiCall('save', { path: saveFilename.value })
  if (res) statusMsg.value = `💾 Sauvegardé : ${res.path}`
}

onMounted(() => {
  fetchFiles()
})
</script>

<template>
  <div class="viewer">
    <div class="header">
        <h2>Data Filter UI</h2>
        <span class="status-badge">{{ statusMsg }}</span>
    </div>
    
    <div class="controls-wrapper">
      
      <div class="panel">
        <h3>📂 Fichier</h3>
        <div class="group">
          <select v-model="selectedFile" @change="getPreview">
            <option disabled value="">-- Choisir --</option>
            <option v-for="f in availableFiles" :key="f" :value="f">{{ f }}</option>
          </select>
          <button @click="loadData" class="btn-primary">Charger</button>
        </div>
        
        <div v-if="filePreview" class="preview-box">
            <h4>Aperçu du fichier (10 premières lignes) :</h4>
            <pre>{{ filePreview }}</pre>
        </div>
      </div>

      <div class="panel">
        <h3>🔍 Filtre</h3>
        <div class="group">
          <input v-model="filterField" placeholder="Colonne" class="input-sm" />
          <input v-model="filterValue" placeholder="Valeur" class="input-sm" />
          <button @click="applyFilter">Filtrer</button>
        </div>
      </div>

      <div class="panel">
        <h3>🛠️ Outils</h3>
        <div class="group">
          <button @click="getStats" class="btn-info">📊 Stats</button>
          <div class="save-box">
            <input v-model="saveFilename" placeholder="Nom fichier" class="input-sm" />
            <button @click="saveFile" class="btn-save">💾 Sauver</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showStats && statsReport" class="stats-container">
      <div class="stats-header">
        <h3>Statistiques</h3>
        <button class="close-btn" @click="showStats = false">Fermer</button>
      </div>
      <div class="stats-grid">
        <div v-for="(info, field) in statsReport" :key="field" class="stat-card">
          <h4>{{ field }}</h4>
          <div>Non-null: {{ info.non_null_count }}</div>
          <div>Null: {{ info.null_count }}</div>
        </div>
      </div>
    </div>

    <div class="table-container" v-if="tableData.length">
      <table>
        <thead>
          <tr>
            <th v-for="(val, key) in tableData[0]" :key="key" @click="sortCol(key)">
              {{ key }} ↕
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, i) in tableData" :key="i">
            <td v-for="(val, key) in row" :key="key">
              {{ typeof val === 'object' ? JSON.stringify(val) : val }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.viewer { 
  max-width: 1200px; 
  margin: 0 auto; 
  font-family: sans-serif; 
  padding: 20px; 
}
.header { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  margin-bottom: 20px; 
  border-bottom: 2px solid #333; 
  padding-bottom: 10px;
}
.status-badge { 
  background: #333; 
  padding: 5px 10px; 
  border-radius: 4px; 
  color: #42b983; 
  font-weight: bold; 
}

.preview-box {
    margin-top: 15px;
    background: #111;
    padding: 10px;
    border-radius: 4px;
    border: 1px dashed #555;
}
.preview-box h4 { margin: 0 0 5px 0; font-size: 0.8em; color: #888; }
.preview-box pre {
    margin: 0;
    font-size: 0.8em;
    color: #ccc;
    white-space: pre-wrap;
    max-height: 150px;
    overflow-y: auto;
    font-family: monospace;
}

.controls-wrapper { 
  display: flex; 
  gap: 15px; 
  flex-wrap: wrap;
   margin-bottom: 20px;
}
.panel { 
  background: #222; 
  padding: 15px; 
  border-radius: 8px; 
  flex: 1; 
  min-width: 250px; 
  border: 1px solid #444;
}
.panel h3 { 
  margin: 0 0 10px 0; 
  color: #aaa; 
  font-size: 0.9em; 
  text-transform: uppercase; 
}

.group { 
  display: flex; 
  gap: 10px; 
  align-items: center;
}
.save-box { 
  display: flex; 
  gap: 5px; 
  border-left: 1px solid #555; 
  padding-left: 10px; 
  margin-left: 5px;
}

input, select, button { 
  padding: 8px; 
  border-radius: 4px; 
  border: 1px solid #555; 
  background: #333; 
  color: white; 
}
select { 
  flex-grow: 1; 
}
button { 
  cursor: pointer; 
  font-weight: bold; 
}
button:hover { 
  background: #444; 
}

.btn-primary { 
  background: #646cff; 
  border-color: #646cff;
}
.btn-info { 
  background: #3498db; 
  border-color: #3498db; 
}
.btn-save { background: #27ae60;
   border-color: #27ae60;
}

.input-sm {
   width: 100px; 
}

.stats-container { 
  background: #2c3e50; 
  padding: 15px; border-radius: 
  8px; margin-bottom: 20px; 
}
.stats-header { display: flex; 
  justify-content: space-between; 
  margin-bottom: 10px; 
}
.stats-grid { display: grid; 
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 10px; 
}
.stat-card { 
  background: #34495e;
  padding: 10px; 
  border-radius: 5px; 
}

.table-container { 
  overflow-x: auto; 
  border: 1px solid #444; 
  border-radius: 8px; 
}
table { 
  width: 100%; 
  border-collapse: collapse; 
  background: #1e1e1e; 
}
th, td { 
  padding: 10px; 
  text-align: left; 
  border-bottom: 1px solid #333; 
}
th { 
  background: #252525; 
  cursor: pointer; 
}
th:hover { 
  background: #333; 
  }
</style>