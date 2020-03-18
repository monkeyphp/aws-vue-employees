<!--
@file app/src/components/DeleteEmployeeTimesheetForm.vue

This component is used to render a form so that the user can confirm the delete of a Timesheet.
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
                    Are you sure that you want to delete {{ date }}?
                </p>
            </v-card-text>

            <v-card-actions class="justify-center">
                <v-btn color="indigo"  text  v-on:click="cancel()" class="flex-grow-1">Cancel</v-btn>
                <v-btn color="error" :loading="loading" v-on:click="confirm()" class="flex-grow-1">Delete</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
    export default {
        name: 'DeleteEmployeeTimesheetForm',
        props: ['employee_timesheet', 'dialog'],
        watch: {
            employee_timesheet (new_employee_timesheet) {
                if (new_employee_timesheet) {
                    this.initialize()
                }
            }
        },
        data: function () {
            return {
                loading: false,
                title: 'Delete Timesheet',
                date: null,
            };
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
        created() {
            this.initialize();
        },
        methods: {
            initialize() {
                const date = this.employee_timesheet.date;
                this.date = date;
                this.title = `Delete ${date}`;
            },
            cancel () {
                this.close();
                this.reset();
            },
            confirm () {
                this.loading = true;
                this.$store.dispatch('employees/delete_employee_timesheet', this.employee_timesheet)
                    .finally(() => {
                        this.loading = false;
                        this.close();
                    });
            },
            reset () {
                this.title = 'Delete Timesheet';
            },
            close () {
                this.$emit('update-dialog', false);
            },
        }
    }
</script>