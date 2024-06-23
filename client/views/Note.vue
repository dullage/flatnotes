<template>
  <!-- Confirm Deletion Modal -->
  <ConfirmModal
    v-model="isDeleteModalVisible"
    title="Confirm Deletion"
    :message="`Are you sure you want to delete the note '${note.title}'?`"
    confirmButtonText="Delete"
    confirmButtonStyle="danger"
    @confirm="deleteConfirmedHandler"
  />

  <!-- Confirm Cancellation Modal -->
  <ConfirmModal
    v-model="isCancellationModalVisible"
    title="Confirm Closure"
    message="Changes have been made. Are you sure you want to close the note?"
    confirmButtonText="Close"
    confirmButtonStyle="danger"
    @confirm="cancelConfirmedHandler"
  />

  <!-- Draft Modal -->
  <ConfirmModal
    v-model="isDraftModalVisible"
    title="Draft Detected"
    message="There is an unsaved draft of this note stored in this browser. Do you want to resume the draft version or delete it?"
    confirmButtonText="Resume Draft"
    confirmButtonStyle="cta"
    cancelButtonText="Delete Draft"
    cancelButtonStyle="danger"
    @confirm="setEditMode()"
    @cancel="
      clearDraft();
      setEditMode();
    "
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
          class="w-full bg-theme-background outline-none"
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
      <ToastViewer
        v-if="!editMode"
        :initialValue="note.content"
        class="toast-viewer"
      />
      <ToastEditor
        v-if="editMode"
        ref="toastEditor"
        :initialValue="getInitialEditorValue()"
        :initialEditType="loadDefaultEditorMode()"
        :addImageBlobHook="addImageBlobHook"
        @change="startDraftSaveTimeout"
      />
    </div>
  </LoadingIndicator>
</template>

<style>
/* Disable checkboxes in view mode. See https://github.com/nhn/tui.editor/issues/1087. */
.toast-viewer li.task-list-item {
  pointer-events: none;
}
.toast-viewer li.task-list-item a {
  pointer-events: auto;
}
</style>


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
  createAttachment,
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
let draftSaveTimeout = null;
const editMode = ref(false);
const globalStore = useGlobalStore();
const isCancellationModalVisible = ref(false);
const isDeleteModalVisible = ref(false);
const isDraftModalVisible = ref(false);
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
  // Return if we already have the note e.g. When we rename a note, the route prop would change but we’d already have the note.
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

// Note Editing
function editHandler() {
  const draftContent = loadDraft();
  if (draftContent) {
    isDraftModalVisible.value = true;
  } else {
    setEditMode();
  }
}

function setEditMode() {
  setBeforeUnloadConfirmation(true);
  newTitle.value = note.value.title;
  editMode.value = true;
}

function getInitialEditorValue() {
  const draftContent = loadDraft();
  return draftContent ? draftContent : note.value.content;
}

// Note Deletion
function deleteHandler() {
  isDeleteModalVisible.value = true;
}

function deleteConfirmedHandler() {
  deleteNote(note.value.title)
    .then(() => {
      toast.add(getToastOptions("Note deleted ✓", "Success", "success"));
      router.push({ name: "home" });
    })
    .catch((error) => {
      apiErrorHandler(error, toast);
    });
}

// Note Edit Cancellation
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

function cancelConfirmedHandler() {
  clearDraft();
  setBeforeUnloadConfirmation(false);
  editMode.value = false;
  if (!props.title) {
    router.push({ name: "home" });
  } else {
    editMode.value = false;
  }
}

// Note Saving
function saveHandler() {
  // Save Default Editor Mode
  saveDefaultEditorMode();

  // Empty Title Validation
  if (!newTitle.value) {
    toast.add(
      getToastOptions("Cannot save note without a title.", "Invalid", "error"),
    );
    return;
  }

  // Invalid Character Validation
  if (reservedFilenameCharacters.test(newTitle.value)) {
    badFilenameToast("Title");
    return;
  }

  // Save Note
  let newContent = toastEditor.value.getMarkdown();
  if (isNewNote.value) {
    saveNew(newTitle.value, newContent);
  } else {
    saveExisting(newTitle.value, newContent);
  }
}

function saveNew(newTitle, newContent) {
  createNote(newTitle, newContent)
    .then((data) => {
      clearDraft();
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
      clearDraft();
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
        "A note with this title already exists. Please try again with a new title.",
        "Duplicate",
        "error",
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
  toast.add(getToastOptions("Note saved successfully ✓", "Success", "success"));
}

// Image Upload
function addImageBlobHook(file, callback) {
  const altTextInputValue = document.getElementById(
    "toastuiAltTextInput",
  )?.value;

  // Upload the image then use the callback to insert the URL into the editor
  postAttachment(file).then(function (data) {
    if (data) {
      // If the user has entered an alt text, use it. Otherwise, use the filename returned by the API.
      const altText = altTextInputValue ? altTextInputValue : data.filename;
      callback(data.url, altText);
    }
  });
}

function postAttachment(file) {
  // Invalid Character Validation
  if (reservedFilenameCharacters.test(file.name)) {
    badFilenameToast("Title");
    return;
  }

  // Uploading Toast
  toast.add(getToastOptions("Uploading attachment..."));

  // Upload the attachment
  return createAttachment(file)
    .then((data) => {
      // Success Toast
      toast.add(
        getToastOptions(
          "Attachment uploaded successfully ✓",
          "Success",
          "success",
        ),
      );
      return data;
    })
    .catch((error) => {
      if (error.response?.status === 409) {
        // Note: The current implementation will append a datetime to the filename if it already exists.
        // Error Toast
        toast.add(
          getToastOptions(
            "An attachment with this filename already exists.",
            "Duplicate",
            "error",
          ),
        );
      } else if (error.response?.status == 413) {
        entityTooLargeToast("attachment");
      } else {
        apiErrorHandler(error, toast);
      }
    });
}

// Drafts
function clearDraftSaveTimeout() {
  if (draftSaveTimeout != null) {
    clearTimeout(draftSaveTimeout);
  }
}

function saveDraft() {
  const content = toastEditor.value.getMarkdown();
  if (content) {
    localStorage.setItem(note.value.title, content);
  }
}

function startDraftSaveTimeout() {
  clearDraftSaveTimeout();
  draftSaveTimeout = setTimeout(saveDraft, 1000);
}

function clearDraft() {
  localStorage.removeItem(note.value.title);
}

function loadDraft() {
  return localStorage.getItem(note.value.title);
}

// Helpers
function entityTooLargeToast(entityName) {
  toast.add(
    getToastOptions(
      `This ${entityName} is too large. Please try again with a smaller ${entityName} or adjust your server configuration.`,
      "Failure",
      "error",
    ),
  );
}

function badFilenameToast(entityName) {
  toast.add(
    getToastOptions(
      'Due to filename restrictions, the following characters are not allowed: <>:"/\\|?*',
      `Invalid ${entityName}`,
      "error",
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

function saveDefaultEditorMode() {
  const isWysiwygMode = toastEditor.value.isWysiwygMode();
  localStorage.setItem(
    "defaultEditorMode",
    isWysiwygMode ? "wysiwyg" : "markdown",
  );
}

function loadDefaultEditorMode() {
  const defaultWysiwygMode = localStorage.getItem("defaultEditorMode");
  return defaultWysiwygMode || "markdown";
}

watch(() => props.title, init);
onMounted(init);
</script>
