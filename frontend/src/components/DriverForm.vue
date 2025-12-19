<script setup>
import { ref } from 'vue';

const props = defineProps({
  driver: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['submit', 'cancel']);

const form = ref({
  name: props.driver?.name || '',
  color: props.driver?.color || '#90CAF9',
  password: ''
});

const isEdit = !!props.driver;

function handleSubmit() {
  if (!form.value.name || (!isEdit && !form.value.password)) {
    return;
  }
  emit('submit', form.value);
}

function handleCancel() {
  emit('cancel');
}
</script>

<template>
  <div class="modal-overlay" @click.self="handleCancel">
    <div class="modal-content">
      <div class="modal-header">
        <h2>{{ isEdit ? 'Edit Driver' : 'Add New Driver' }}</h2>
      </div>
      <button class="close-btn" @click="handleCancel">
        <svg viewBox="0 0 24 24" fill="none" style="width: 20px; height: 20px;">
          <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" fill="currentColor"/>
        </svg>
      </button>
      
      <div class="modal-body">
        <div class="form-section">
          <label>Driver Name *</label>
          <input 
            type="text" 
            v-model="form.name" 
            placeholder="Enter driver name"
            maxlength="50"
            autofocus
          >
        </div>
        
        <div class="form-section">
          <label>Identification Color *</label>
          <div class="color-picker-wrapper">
            <input type="color" v-model="form.color" class="color-picker">
            <div class="color-preview" :style="{ background: form.color }"></div>
            <span class="color-value">{{ form.color }}</span>
          </div>
          <small>Choose a unique color to identify this driver</small>
        </div>
        
        <div class="form-section">
          <label>Password {{ isEdit ? '(leave blank to keep current)' : '*' }}</label>
          <input 
            type="password" 
            v-model="form.password" 
            :placeholder="isEdit ? 'Enter new password to change' : 'Enter password'"
            autocomplete="new-password"
          >
          <small>{{ isEdit ? 'Only enter a password if you want to change it' : 'This will be used for driver authentication' }}</small>
        </div>
      </div>
      
      <div class="modal-footer">
        <button @click="handleCancel" class="btn-secondary">
          Cancel
        </button>
        <button 
          @click="handleSubmit" 
          class="btn-primary"
          :disabled="!form.name || (!isEdit && !form.password)"
        >
          <svg viewBox="0 0 24 24" fill="none" style="width: 18px; height: 18px; margin-right: 8px;">
            <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z" fill="currentColor"/>
          </svg>
          {{ isEdit ? 'Update Driver' : 'Create Driver' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: var(--md-sys-color-surface-container-low);
  border-radius: var(--md-shape-corner-xlarge);
  box-shadow: var(--md-elevation-3);
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow: auto;
  position: relative;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: var(--md-spacing-lg);
  border-bottom: 1px solid var(--md-sys-color-outline-variant);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.close-btn {
  position: absolute;
  top: 0;
  right: 0;
  background: #ef5350;
  border: none;
  cursor: pointer;
  width: 40px;
  height: 40px;
  border-radius: 0 var(--md-shape-corner-xlarge) 0 0;
  color: white;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: #d32f2f;
}

.modal-body {
  padding: var(--md-spacing-lg);
}

.form-section {
  margin-bottom: var(--md-spacing-lg);
}

.form-section:last-child {
  margin-bottom: 0;
}

.form-section label {
  display: block;
  margin-bottom: var(--md-spacing-sm);
  font-weight: 600;
  color: var(--md-sys-color-on-surface);
}

.form-section small {
  display: block;
  margin-top: var(--md-spacing-xs);
  color: var(--md-sys-color-on-surface-variant);
  font-size: 0.875rem;
}

.color-picker-wrapper {
  display: flex;
  align-items: center;
  gap: var(--md-spacing-md);
  padding: var(--md-spacing-md);
  background: var(--md-sys-color-surface-container);
  border-radius: var(--md-shape-corner-small);
  margin-bottom: var(--md-spacing-xs);
}

.color-picker {
  width: 60px;
  height: 48px;
  border: none;
  border-radius: var(--md-shape-corner-small);
  cursor: pointer;
}

.color-preview {
  width: 48px;
  height: 48px;
  border-radius: var(--md-shape-corner-small);
  box-shadow: var(--md-elevation-1);
}

.color-value {
  font-family: 'Courier New', monospace;
  font-weight: 600;
  color: var(--md-sys-color-on-surface-variant);
  text-transform: uppercase;
  flex: 1;
}

.modal-footer {
  display: flex;
  gap: var(--md-spacing-md);
  padding: var(--md-spacing-lg);
  border-top: 1px solid var(--md-sys-color-outline-variant);
  justify-content: flex-end;
}

.btn-secondary {
  background: var(--md-sys-color-surface-container-high);
  color: var(--md-sys-color-on-surface);
  border: none;
  padding: 12px 24px;
  border-radius: var(--md-shape-corner-xlarge);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-secondary:hover {
  background: var(--md-sys-color-surface-container-highest);
}

.btn-primary {
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  border: none;
  padding: 12px 24px;
  border-radius: var(--md-shape-corner-xlarge);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-primary:hover:not(:disabled) {
  background: var(--md-sys-color-primary-container);
  color: var(--md-sys-color-on-primary-container);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--md-sys-color-outline);
  border-radius: var(--md-shape-corner-small);
  background: var(--md-sys-color-surface-container);
  color: var(--md-sys-color-on-surface);
  font-size: 1rem;
  font-family: inherit;
  transition: all 0.2s;
  box-sizing: border-box;
}

input[type="text"]:focus,
input[type="password"]:focus {
  outline: none;
  border-color: var(--md-sys-color-primary);
  background: var(--md-sys-color-surface-container-high);
}
</style>
