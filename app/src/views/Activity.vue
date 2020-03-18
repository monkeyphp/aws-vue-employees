<!--
@file app/src/views/Activity.vue

This component is used to render an Activity.
-->
<template>
    <v-app v-bind:id="id">

        <v-app-bar app color="indigo" dark>
            <v-btn icon v-bind:to="{name: 'admin', query: {tab: 'activities'}}">
                <v-icon>mdi-arrow-left</v-icon>
            </v-btn>

            <v-toolbar-title>{{ activity.name }}</v-toolbar-title>
            <v-spacer></v-spacer>

            <v-btn icon v-on:click.stop="open_edit_activity_dialog()">
                <v-icon>mdi-pencil</v-icon>
            </v-btn>

            <v-btn icon v-on:click.stop="open_delete_activity_dialog()">
                <v-icon>mdi-delete</v-icon>
            </v-btn>

            <v-menu left bottom>
                <template v-slot:activator="{ on }">
                    <v-btn icon v-on="on">
                        <v-icon>mdi-dots-vertical</v-icon>
                    </v-btn>
                </template>
                <v-list>
                    <v-list-item>
                        <v-list-item-title>Settings</v-list-item-title>
                    </v-list-item>
                    <v-list-item>
                        <v-list-item-title>About</v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>
        </v-app-bar>

        <v-content>
            <v-container fluid no-gutters class="pa-0">
                <v-list>
                    <v-list-item two-line>
                        <v-list-item-content>
                            <v-list-item-title>Name</v-list-item-title>
                            <v-list-item-subtitle>{{ activity.name }}</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>

                    <v-list-item two-line>
                        <v-list-item-content>
                            <v-list-item-title>Code</v-list-item-title>
                            <v-list-item-subtitle>{{ activity.code }}</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>

                    <v-list-item two-line>
                        <v-list-item-content>
                            <v-list-item-title>Worked</v-list-item-title>
                            <v-list-item-subtitle>{{ activity.worked }}</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>

                    <v-list-item two-line>
                        <v-list-item-content>
                            <v-list-item-title>Description</v-list-item-title>
                            <v-list-item-subtitle>{{ activity.description }}</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>

                <EditActivityDialog v-bind:activity="activity"
                               v-bind:dialog="edit_activity_dialog"
                               v-on:update-dialog="close_edit_activity_dialog()" />

                <DeleteActivityDialog v-bind:activity="activity"
                                 v-bind:dialog="delete_activity_dialog"
                                 v-on:update-dialog="close_delete_activity_dialog()" />
            </v-container>
        </v-content>
    </v-app>
</template>

<script>
import EditActivityDialog from '@/components/EditActivityDialog.vue';
import DeleteActivityDialog from '@/components/DeleteActivityDialog.vue';

export default {
    name: 'Activity',
    props: ['activity_id'],
    components: {
        EditActivityDialog,
        DeleteActivityDialog
    },
    watch: {
        activity_id (new_activity_id) {
            if (new_activity_id) {
                this.initialize();
            }
        },
    },
    created () {
        this.initialize();
    },
    computed: {
        activity() {
            let _activity= null;
            if (this.activity_id) {
                _activity = this.$store.getters['activities/activity'](this.activity_id);
            }
            return _activity;
        }
    },
    methods: {
        initialize () {
            if (this.activity_id) {
                this.loading = true;
                this.$store.dispatch('activities/get_activity', this.activity_id)
                    .finally(() => {
                        this.loading = false;
                    })
            }
        },

        open_edit_activity_dialog () {
            this.edit_activity_dialog = true;
        },

        close_edit_activity_dialog () {
            this.edit_activity_dialog = false;
        },

        open_delete_activity_dialog () {
            this.delete_activity_dialog = true;
        },

        close_delete_activity_dialog () {
            this.delete_activity_dialog = false;
        },
    },
    data: function () {
        return {
            id: 'activity',
            title: 'Activity',
            loading: false,
            loading_text: 'Loading Activity... please wait',
            edit_activity_dialog: false,
            delete_activity_dialog: false,
        };
    },
};
</script>