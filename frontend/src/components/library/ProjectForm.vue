<template>
  <el-dialog
    v-model="visible"
    :title="isEdit ? '编辑项目' : '新建项目'"
    width="500px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="80px"
      class="project-form"
    >
      <el-form-item label="项目名称" prop="name">
        <el-input
          v-model="form.name"
          placeholder="请输入项目名称"
          maxlength="100"
          show-word-limit
        />
      </el-form-item>
      
      <el-form-item label="项目描述" prop="description">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="4"
          placeholder="请输入项目描述（可选）"
          maxlength="1000"
          show-word-limit
        />
      </el-form-item>
    </el-form>
    
    <template #footer>
      <el-button @click="handleClose">取消</el-button>
      <el-button type="primary" :loading="loading" @click="handleSubmit">
        {{ isEdit ? '保存' : '创建' }}
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import type { Project, ProjectCreateRequest, ProjectUpdateRequest } from '@/types/project'
import { useProjectStore } from '@/stores/projects'

const props = defineProps<{
  modelValue: boolean
  project?: Project | null
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  success: []
}>()

const projectStore = useProjectStore()
const formRef = ref<FormInstance>()
const loading = ref(false)

const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const isEdit = computed(() => !!props.project)

const form = ref<ProjectCreateRequest & ProjectUpdateRequest>({
  name: '',
  description: ''
})

const rules: FormRules = {
  name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' },
    { min: 1, max: 100, message: '项目名称长度应在1-100个字符之间', trigger: 'blur' }
  ]
}

watch(() => props.project, (newVal) => {
  if (newVal) {
    form.value = {
      name: newVal.name,
      description: newVal.description || ''
    }
  } else {
    form.value = {
      name: '',
      description: ''
    }
  }
}, { immediate: true })

const handleClose = () => {
  visible.value = false
  formRef.value?.resetFields()
}

const handleSubmit = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  try {
    if (isEdit.value && props.project) {
      await projectStore.updateProject(props.project.id, {
        name: form.value.name,
        description: form.value.description || undefined
      })
      ElMessage.success('项目更新成功')
    } else {
      await projectStore.createProject({
        name: form.value.name,
        description: form.value.description || undefined
      })
      ElMessage.success('项目创建成功')
    }
    emit('success')
    handleClose()
  } catch (error) {
    ElMessage.error(isEdit.value ? '项目更新失败' : '项目创建失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.project-form {
  padding: 20px 0;
}
</style>
