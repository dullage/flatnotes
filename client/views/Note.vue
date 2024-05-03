<template>
  <div class="h-full">
    <!-- Loading -->
    <LoadingIndicator
      v-if="showLoadingIndicator"
      ref="loadingIndicator"
      class="flex h-full items-center justify-center"
    />

    <!-- Loaded -->
    <div v-else>
      <!-- Confirm Deletion Modal -->
      <ConfirmModal
        ref="deleteConfirmModal"
        title="Confirm Deletion"
        :message="`Are you sure you want to delete the note '${note.title}'?`"
        isDanger
        @confirm="deleteConfirmedHandler"
      />

      <!-- Header -->
      <div class="flex items-end">
        <!-- View -->
        <div v-show="!editMode" class="flex-1 text-3xl">{{ note.title }}</div>
        <div v-show="!editMode">
          <CustomButton
            :iconPath="mdilDelete"
            label="Delete"
            @click="deleteHandler"
          />
          <CustomButton
            :iconPath="mdilPencil"
            label="Edit"
            @click="editHandler"
          />
        </div>

        <!-- Edit -->
        <input
          v-show="editMode"
          v-model="noteUpdate.title"
          class="flex-1 text-3xl"
          placeholder="Title"
        />
        <div v-show="editMode">
          <CustomButton
            :iconPath="mdilArrowLeft"
            label="Cancel"
            @click="cancelHandler"
          />
          <CustomButton
            :iconPath="mdilContentSave"
            label="Save"
            @click="saveHandler"
          />
        </div>
      </div>

      <hr class="my-4 border-theme-border" />

      <!-- Content -->
      <ToastViewer v-if="!editMode" :initialValue="note.content" />
    </div>
  </div>
</template>

<script setup>
import { mdiNoteOffOutline } from "@mdi/js";
import {
  mdilArrowLeft,
  mdilContentSave,
  mdilDelete,
  mdilPencil,
} from "@mdi/light-js";
import { useToast } from "primevue/usetoast";
import { ref, watch } from "vue";
import { useRouter } from "vue-router";

import { deleteNote, getNote } from "../api.js";
import { Note } from "../classes.js";
import ConfirmModal from "../components/ConfirmModal.vue";
import CustomButton from "../components/CustomButton.vue";
import LoadingIndicator from "../components/LoadingIndicator.vue";
import ToastViewer from "../components/Toast/ToastViewer.vue";
import { getUnknownServerErrorToastOptions } from "../helpers.js";

const props = defineProps({
  title: String,
});

const editMode = ref(false);
const deleteConfirmModal = ref();
const loadingIndicator = ref();
const note = ref({});
const noteUpdate = ref({});
const router = useRouter();
const showLoadingIndicator = ref(true);
const toast = useToast();

function init() {
  showLoadingIndicator.value = true;
  if (props.title) {
    getNote(props.title)
      .then((data) => {
        note.value = data;
        showLoadingIndicator.value = false;
      })
      .catch((error) => {
        if (error.response.status === 404) {
          loadingIndicator.value.setFailed("Note not found", mdiNoteOffOutline);
        } else {
          loadingIndicator.value.setFailed();
          toast.add(getUnknownServerErrorToastOptions());
        }
      });
  } else {
    editMode.value = true;
    note.value = new Note();
    showLoadingIndicator.value = false;
  }
}

function editHandler() {
  noteUpdate.value = { ...note.value };
  editMode.value = true;
}

function deleteHandler() {
  deleteConfirmModal.value.toggle();
}

function deleteConfirmedHandler() {
  deleteNote(note.value.title)
    .then(() => {
      router.push({ name: "home" });
    })
    .catch(() => {
      toast.add(getUnknownServerErrorToastOptions());
    });
}

function cancelHandler() {
  editMode.value = false;
  if (!props.title) {
    router.push({ name: "home" });
  } else {
    editMode.value = false;
  }
}

function saveHandler() {
  editMode.value = false;
}

watch(() => props.title, init, { immediate: true });
</script>
