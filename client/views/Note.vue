<template>
  <!-- Confirm Deletion Modal -->
  <ConfirmModal
    v-model="isDeleteModalVisible"
    title="Confirm Deletion"
    :message="`Are you sure you want to delete the note '${note.title}'?`"
    confirmButtonText="Delete"
    isDanger
    @confirm="deleteConfirmedHandler"
  />

  <!-- Confirm Cancellation Modal -->
  <ConfirmModal
    v-model="isCancellationModalVisible"
    title="Confirm Closure"
    :message="`Changes have been made. Are you sure you want to close the note '${note.title}'?`"
    confirmButtonText="Close"
    isDanger
    @confirm="cancelConfirmedHandler"
  />

  <LoadingIndicator ref="loadingIndicator" class="flex h-full flex-col">
    <!-- Header -->
    <div class="flex flex-col-reverse md:flex-row md:items-baseline">
      <!-- Title -->
      <div class="grow truncate text-3xl leading-[1.6em]">
        <span v-show="!editMode" :title="note.title">{{ note.title }}</span>
        <input
          v-show="editMode"
          v-model.trim="newTitle"
          class="flex-1 bg-theme-background outline-none"
          placeholder="Title"
        />
      </div>

      <!-- Buttons -->
      <div class="flex shrink-0 self-end md:self-baseline">
        <div v-show="!editMode">
          <CustomButton
            v-if="canModify"
            :iconPath="mdilDelete"
            label="Delete"
            @click="deleteHandler"
          />
          <CustomButton
            v-if="canModify"
            class="ml-1"
            :iconPath="mdilPencil"
            label="Edit"
            @click="editHandler"
          />
        </div>
        <div v-show="editMode">
          <CustomButton
            :iconPath="mdilArrowLeft"
            label="Cancel"
            @click="cancelHandler"
          />
          <CustomButton
            class="ml-1"
            :iconPath="mdilContentSave"
            label="Save"
            @click="saveHandler"
          />
        </div>
      </div>
    </div>

    <hr v-if="!editMode" class="my-4 border-theme-border" />

    <!-- Content -->
    <div class="flex-1">
      <ToastViewer v-if="!editMode" :initialValue="note.content" />
      <ToastEditor
        v-if="editMode"
        ref="toastEditor"
        :initialValue="note.content"
      />
    </div>
  </LoadingIndicator>
</template>

<script setup>
import { mdiNoteOffOutline } from "@mdi/js";
import {
  mdilArrowLeft,
  mdilContentSave,
  mdilDelete,
  mdilPencil,
} from "@mdi/light-js";
import Mousetrap from "mousetrap";
import { useToast } from "primevue/usetoast";
import { computed, onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";

import {
  apiErrorHandler,
  createNote,
  deleteNote,
  getNote,
  updateNote,
} from "../api.js";
import { Note } from "../classes.js";
import ConfirmModal from "../components/ConfirmModal.vue";
import CustomButton from "../components/CustomButton.vue";
import LoadingIndicator from "../components/LoadingIndicator.vue";
import ToastEditor from "../components/toastui/ToastEditor.vue";
import ToastViewer from "../components/toastui/ToastViewer.vue";
import { authTypes } from "../constants.js";
import { useGlobalStore } from "../globalStore.js";
import { getToastOptions } from "../helpers.js";

const props = defineProps({
  title: String,
});

const canModify = computed(() => globalStore.authType != authTypes.readOnly);
const editMode = ref(false);
const globalStore = useGlobalStore();
const isCancellationModalVisible = ref(false);
const isDeleteModalVisible = ref(false);
const isNewNote = computed(() => !props.title);
const loadingIndicator = ref();
const note = ref({});
const reservedFilenameCharacters = /[<>:"/\\|?*]/;
const router = useRouter();
const newTitle = ref();
const toast = useToast();
const toastEditor = ref();

// 'e' to edit
Mousetrap.bind("e", () => {
  if (editMode.value === false && canModify.value) {
    editHandler();
  }
});

function init() {
  // Return if we already have the note
  if (props.title && props.title == note.value.title) {
    return;
  }

  loadingIndicator.value.setLoading();
  if (props.title) {
    getNote(props.title)
      .then((data) => {
        note.value = data;
        loadingIndicator.value.setLoaded();
      })
      .catch((error) => {
        if (error.response?.status === 404) {
          loadingIndicator.value.setFailed("Note not found", mdiNoteOffOutline);
        } else {
          loadingIndicator.value.setFailed();
          apiErrorHandler(error, toast);
        }
      });
  } else {
    newTitle.value = "";
    note.value = new Note();
    editHandler();
    loadingIndicator.value.setLoaded();
  }
}

// Helpers
function entityTooLargeToast(entityName) {
  toast.add(
    getToastOptions(
      "Failure",
      `This ${entityName} is too large. Please try again with a smaller ${entityName} or adjust your server configuration.`,
      true,
    ),
  );
}

function badFilenameToast(entityName) {
  toast.add(
    getToastOptions(
      `Invalid ${entityName}`,
      'Due to filename restrictions, the following characters are not allowed: <>:"/\\|?*',
      true,
    ),
  );
}

function setBeforeUnloadConfirmation(enable = true) {
  if (enable) {
    window.onbeforeunload = () => {
      return true;
    };
  } else {
    window.onbeforeunload = null;
  }
}

// Button Handlers
function editHandler() {
  setBeforeUnloadConfirmation(true);
  newTitle.value = note.value.title;
  editMode.value = true;
}

function deleteHandler() {
  isDeleteModalVisible.value = true;
}

function cancelHandler() {
  if (
    newTitle.value != note.value.title ||
    toastEditor.value.getMarkdown() != note.value.content
  ) {
    isCancellationModalVisible.value = true;
  } else {
    cancelConfirmedHandler();
  }
}

function saveHandler() {
  // Empty Title Validation
  if (!newTitle.value) {
    toast.add(
      getToastOptions("Invalid", "Cannot save note without a title", true),
    );
    return;
  }

  // Invalid Character Validation
  if (reservedFilenameCharacters.test(newTitle.value)) {
    badFilenameToast("Title");
    return;
  }

  let newContent = toastEditor.value.getMarkdown();
  if (isNewNote.value) {
    saveNew(newTitle.value, newContent);
  } else {
    saveExisting(newTitle.value, newContent);
  }
}

// Additional Logic
function cancelConfirmedHandler() {
  setBeforeUnloadConfirmation(false);
  editMode.value = false;
  if (!props.title) {
    router.push({ name: "home" });
  } else {
    editMode.value = false;
  }
}

function deleteConfirmedHandler() {
  deleteNote(note.value.title)
    .then(() => {
      toast.add(getToastOptions("Success", "Note deleted."));
      router.push({ name: "home" });
    })
    .catch((error) => {
      apiErrorHandler(error, toast);
    });
}

function saveNew(newTitle, newContent) {
  createNote(newTitle, newContent)
    .then((data) => {
      note.value = data;
      router.push({ name: "note", params: { title: note.value.title } });
      noteSaveSuccess();
    })
    .catch(noteSaveFailure);
}

function saveExisting(newTitle, newContent) {
  // Return if no changes
  if (newTitle == note.value.title && newContent == note.value.content) {
    noteSaveSuccess();
    return;
  }

  updateNote(note.value.title, newTitle, newContent)
    .then((data) => {
      note.value = data;
      router.replace({ name: "note", params: { title: note.value.title } });
      noteSaveSuccess();
    })
    .catch(noteSaveFailure);
}

function noteSaveFailure(error) {
  if (error.response?.status === 409) {
    toast.add(
      getToastOptions(
        "Duplicate",
        "A note with this title already exists. Please try again with a new title.",
        true,
      ),
    );
  } else if (error.response?.status === 413) {
    entityTooLargeToast("note");
  } else {
    apiErrorHandler(error, toast);
  }
}

function noteSaveSuccess() {
  setBeforeUnloadConfirmation(false);
  editMode.value = false;
  toast.add(getToastOptions("Success", "Note saved successfully."));
}

watch(() => props.title, init);
onMounted(init);
</script>
