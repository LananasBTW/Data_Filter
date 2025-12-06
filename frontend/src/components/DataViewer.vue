<script setup>
import { ref, onMounted } from 'vue'

const availableFiles = ref([])
const selectedFile = ref('')
const tableData = ref([])
const statusMsg = ref('')

const filterField = ref('')
const filterValue = ref('')
const saveFilename = ref('export.json')

const statsReport = ref(null)
const showStats = ref(false)

const API_URL = 'http://127.0.0.1:8000/api'

async function apiCall(endpoint, payload = null, method = 'POST') {
  statusMsg.value = "Chargement..."
  try {
    const options = {
      method: method,
      headers: { 'Content-Type': 'application/json' },
    }
    if (payload) options.body = JSON.stringify(payload)

    const response = await fetch(`${API_URL}/${endpoint}/`, options)
    const data = await response.json()
    
    if (data.status === 'error') throw new Error(data.message)
    
    statusMsg.value = "Succès !"
    return data
  } catch (e) {
    statusMsg.value = "Erreur : " + e.message
    console.error(e)
    return null
  }
}

// --- Actions ---

// 1. Récupérer la liste des fichiers
async function fetchFiles() {
  const res = await apiCall('files', null, 'GET')
  if (res && res.files) {
    availableFiles.value = res.files
    if (res.files.length > 0) selectedFile.value = res.files[0]
  }
}

// 2. Charger le fichier sélectionné
async function loadData() {
  if (!selectedFile.value) return
  statsReport.value = null // Reset stats
  showStats.value = false
  const res = await apiCall('load', { path: selectedFile.value })
  if (res) tableData.value = res.data
}

// 3. Filtrer
async function applyFilter() {
  const res = await apiCall('filter', { field: filterField.value, value: filterValue.value })
  if (res) tableData.value = res.data
}

// 4. Trier
async function sortCol(colName) {
  const res = await apiCall('sort', { field: colName })
  if (res) tableData.value = res.data
}

// 5. Statistiques
async function loadStats() {
  const res = await apiCall('stats', null, 'GET')
  if (res) {
    statsReport.value = res.report
    showStats.value = true
  }
}

// 6. Sauvegarder
async function saveFile() {
  const res = await apiCall('save', { path: saveFilename.value })
  if (res) {
    statusMsg.value = `Sauvegardé sous : ${res.path}`
  }
}

// Initialisation
onMounted(() => {
  fetchFiles()
})
</script>

<template>
  <div class="viewer">
    <div class="header">
      <h2>Data Filter UI</h2>
      <p class="status">{{ statusMsg }}</p>
    </div>
    
    <div class="controls-container">
      
      <div class="panel">
        <h3>📂 Charger</h3>
        <div class="row">
          <select v-model="selectedFile">
            <option disabled value="">Choisir un fichier</option>
            <option v-for="file in availableFiles" :key="file" :value="file">
              {{ file }}
            </option>
          </select>
          <button @click="loadData" class="btn-primary">Charger</button>
        </div>
      </div>

      <div class="panel">
        <h3>🔍 Filtrer</h3>
        <div class="row">
          <input v-model="filterField" placeholder="Champ (ex: age)" />
          <input v-model="filterValue" placeholder="Valeur (ex: 21)" />
          <button @click="applyFilter">Go</button>
        </div>
      </div>

      <div class="panel">
        <h3>🛠️ Actions</h3>
        <div class="row">
          <button @click="loadStats" class="btn-info">📊 Stats</button>
          <div class="save-group">
            <input v-model="saveFilename" placeholder="Nom fichier" class="input-sm" />
            <button @click="saveFile" class="btn-success">💾 Sauver</button>
          </div>
        </div>
      </div>

    </div>

    <div v-if="showStats && statsReport" class="stats-box">
      <h3>Rapport Statistique</h3>
      <button class="close-btn" @click="showStats = false">Fermer</button>
      <div class="stats-grid">
        <div v-for="(stats, field) in statsReport" :key="field" class="stat-card">
          <h4>{{ field }}</h4>
          <p>Non-null: <strong>{{ stats.non_null_count }}</strong></p>
          <p>Null: <strong>{{ stats.null_count }}</strong></p>
          <div v-for="(tInfo, tName) in stats.type_stats" :key="tName" class="type-info">
             <span class="badge">{{ tName }}</span> : {{ tInfo.count }} items
             <div v-if="tName === 'number'" class="details">
               Moy: {{ tInfo.mean.toFixed(2) }} (Max: {{ tInfo.max }})
             </div>
             <div v-if="tName === 'bool'" class="details">
               Vrai: {{ tInfo.true_percentage.toFixed(0) }}%
             </div>
          </div>
        </div>
      </div>
    </div>

    <div class="table-container" v-if="tableData.length">
      <table>
        <thead>
          <tr>
            <th v-for="(val, key) in tableData[0]" :key="key" @click="sortCol(key)">
              {{ key }} <span class="sort-icon">↕</span>
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
    <div v-else class="empty-state">
      Aucune donnée à afficher. Veuillez charger un fichier.
    </div>
  </div>
</template>

<style scoped>
.viewer { max-width: 1200px; margin: 0 auto; font-family: 'Segoe UI', sans-serif; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 1px solid #444; padding-bottom: 10px; }
.status { color: #42b983; font-weight: bold; }

.controls-container { display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 20px; }
.panel { background: #2a2a2a; padding: 15px; border-radius: 8px; flex: 1; min-width: 250px; display: flex; flex-direction: column; gap: 10px; }
.panel h3 { margin: 0; font-size: 1rem; color: #aaa; }
.row { display: flex; gap: 10px; align-items: center; }

input, select { padding: 8px; border-radius: 4px; border: 1px solid #555; background: #1e1e1e; color: white; flex: 1; }
button { padding: 8px 16px; border-radius: 4px; border: none; cursor: pointer; font-weight: bold; transition: opacity 0.2s; color: white; background: #444; }
button:hover { opacity: 0.9; }

.btn-primary { background-color: #646cff; }
.btn-info { background-color: #0ea5e9; }
.btn-success { background-color: #10b981; }
.input-sm { max-width: 120px; }

.stats-box { background: #1a1a1a; padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #333; position: relative; }
.close-btn { position: absolute; top: 10px; right: 10px; background: #c0392b; font-size: 0.8rem; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; margin-top: 15px; }
.stat-card { background: #333; padding: 10px; border-radius: 6px; font-size: 0.9rem; }
.badge { background: #555; padding: 2px 6px; border-radius: 4px; font-size: 0.8rem; }
.details { font-size: 0.8rem; color: #ccc; margin-left: 5px; margin-top: 2px;}

.table-container { overflow-x: auto; border-radius: 8px; border: 1px solid #444; }
table { width: 100%; border-collapse: collapse; background: #1e1e1e; }
th, td { padding: 12px; text-align: left; border-bottom: 1px solid #333; }
th { background: #252525; cursor: pointer; user-select: none; color: #ddd; }
th:hover { background: #333; }
tr:hover { background: #2a2a2a; }
.sort-icon { font-size: 0.8em; color: #666; }
.empty-state { text-align: center; padding: 40px; color: #666; font-style: italic; }
</style>