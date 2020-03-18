<!--
@file app/src/components/DeleteActivityForm.vue

This component is used to render a dialog asking for confirmation before deleting the Activity
-->
<template>
    <v-dialog v-model="_dialog" fullscreen hide-overlay transition="dialog-bottom-transition">
        <v-card v-bind:loading="loading" class="d-flex flex-column">
            <v-toolbar dark color="indigo" class="flex-grow-0">
                <v-btn icon dark v-on:click="cancel()">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
                <v-toolbar-title>{{ title }}</v-toolbar-title>
            </v-toolbar>
            <v-card-text class="flex-grow-1 pt-5">
                <p>
                    Are you sure that you want to delete {{ name }}?
                </p>
            </v-card-text>

            <v-card-actions class="justify-center">
                <v-btn color="indigo" text  v-on:click="cancel()" class="flex-grow-1">Cancel</v-btn>
                <v-btn color="error" :loading="loading" v-on:click="confirm()" class="flex-grow-1">Delete</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>
<script>
export default {
    name: 'DeleteActivityDialog',
    props: ['activity', 'dialog'],
    watch: {
        activity (new_activity) {
            if (new_activity) {
                this.initialize();
            }
        }
    },
    computed: {
        _dialog: {
            get: function () {
                return this.dialog;
            },
            set: function (val) {
                this.$emit('update-dialog', val);
            }
        },
    },
    methods: {
        initialize() {
            const name = this.activity.name;
            this.name = name;
            this.title = `Delete ${name}`;
        },
        cancel () {
            this.close();
            this.reset();
        },
        confirm() {
            this.loading = true;
            this.$store.dispatch('activities/delete_activity', this.activity)
                .then(() => {
                    this.loading = false;
                    this.close();
                    this.$router.push({name: 'admin', query: {tab: 'activities'}});
                });
        },
        reset() {
            this.title = 'Delete Activity';
        },
        close() {
            this.$emit('update-dialog', false);
        },
    },
    data: function () {
        return {
            name: null,
            loading: false,
            title: 'Delete Activity',
        };
    },
}
</script>