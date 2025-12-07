<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  files: Array,
  isLoading: Boolean,
  previewText: String
})

const emit = defineEmits(['load-file', 'load-data', 'apply-filter', 'get-stats', 'save-file'])

const selectedFile = ref('')
const filterField = ref('')
const filterValue = ref('')
const saveFilename = ref('export.json')

// Quand l'utilisateur change de fichier dans la liste, on demande la preview
watch(selectedFile, (newVal) => {
  if(newVal) emit('load-file', newVal)
})

// Initialisation : Sélectionner le premier fichier si disponible
watch(() => props.files, (newFiles) => {
  if (newFiles && newFiles.length > 0 && !selectedFile.value) {
    selectedFile.value = newFiles[0]
  }
})
</script>

<template>
  <div class="sidebar">
    
    <div class="card control-card">
      <div class="card-header">
        <svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
        <h3>Fichier Source</h3>
      </div>
      <div class="card-body">
        <select v-model="selectedFile" class="input-normal">
          <option v-for="f in files" :key="f" :value="f">{{ f }}</option>
        </select>
        <button @click="$emit('load-data', selectedFile)" class="btn btn-primary full-width" :disabled="isLoading">
          {{ isLoading ? 'Chargement...' : 'Charger' }}
        </button>
      </div>
      <div v-if="previewText" class="preview-mini">
        <div class="preview-label">Aperçu</div>
        <pre>{{ previewText }}</pre>
      </div>
    </div>

    <div class="card control-card">
      <div class="card-header">
        <svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <h3>Filtres</h3>
      </div>
      <div class="card-body">
        <input v-model="filterField" placeholder="Colonne (ex: age)" class="input-normal input-dark" />
        <input v-model="filterValue" placeholder="Valeur (ex: 25)" class="input-normal input-dark" />
        <button @click="$emit('apply-filter', { field: filterField, value: filterValue })" class="btn btn-secondary full-width">Appliquer</button>
      </div>
    </div>

    <div class="card control-card">
      <div class="card-header">
        <svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path></svg>
        <h3>Actions</h3>
      </div>
      <div class="card-body tools-body">
        <button @click="$emit('get-stats')" class="btn btn-info full-width">
           <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 20V10"></path><path d="M12 20V4"></path><path d="M6 20v-6"></path></svg> Stats
        </button>
        <div class="divider"></div>
        <div class="save-group">
          <input v-model="saveFilename" class="input-normal input-dark" />
          <button @click="$emit('save-file', saveFilename)" class="btn btn-success">
             <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></svg>
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
.sidebar {
    display: flex;
    flex-direction: column;
    gap: 25px;
}

.card {
    background: #1e1e1e;
    border-radius: 12px;
    border: 1px solid #333;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.card-header {
    padding: 15px 20px;
    border-bottom: 1px solid #333;
    background: rgba(255, 255, 255, 0.02);
    display: flex;
    align-items: center;
    gap: 10px;
}

.card-header h3 {
    margin: 0;
    font-size: 0.9rem;
    font-weight: 600;
    color: #aaa;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.card-body {
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.icon { color: #646cff; opacity: 0.9; }

.input-normal {
    width: 100%;
    padding: 10px 12px;
    background: #2a2a2a;
    border: 1px solid #444;
    border-radius: 6px;
    color: white;
    font-family: inherit;
    font-size: 0.9rem;
    box-sizing: border-box;
}

.input-normal:focus {
    outline: none;
    border-color: #646cff;
}

.input-dark { background: #151515; }

.btn {
    border: none;
    padding: 10px 16px;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 0.9rem;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
}

.btn:hover { filter: brightness(110%); transform: translateY(-1px); }
.btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
.full-width { width: 100%; }

.btn-primary { background: #646cff; color: white; }
.btn-secondary { background: #333; color: white; border: 1px solid #444; }
.btn-info { background: #0ea5e9; color: white; }
.btn-success { background: #10b981; color: white; padding: 0 15px; }

.preview-mini {
    background: #000;
    border-top: 1px solid #333;
    padding: 15px;
}

.preview-label {
    font-size: 0.7rem;
    color: #666;
    margin-bottom: 5px;
    text-transform: uppercase;
}

.preview-mini pre {
    margin: 0;
    font-family: monospace;
    font-size: 0.75rem;
    color: #a5b4fc;
    white-space: pre-wrap;
    max-height: 150px;
    overflow-y: auto;
}

.divider { height: 1px; background: #333; margin: 5px 0; }
.save-group { display: flex; gap: 8px; }
.tools-body { gap: 10px; }
</style>