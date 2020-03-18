<!--
@file app/src/components/EditEmployeeTimesheetEntryForm.vue

This component is used to render a form for editing a Timesheet Entry.
-->
<template>
    <v-dialog v-model="_dialog" fullscreen hide-overlay transition="dialog-bottom-transition">
        <v-card v-bind:loading="loading" class="d-flex flex-column">
            <v-toolbar dark color="indigo" class="flex-grow-0">
                <v-btn icon dark @click="cancel()"><v-icon>mdi-close</v-icon></v-btn>
                <v-toolbar-title>{{ title }}</v-toolbar-title>
            </v-toolbar>
            <v-card-text class="flex-grow-1 pt-5">
                <v-form v-model="valid" ref="form">
                    <v-text-field v-model="date"
                                  v-bind:rules="date_rules"
                                  required
                                  label="Date" name="date" type="date"/>
                    <v-text-field v-model="start"
                                  v-bind:rules="start_rules"
                                  required
                                  label="Start Time" name="start" type="time"/>
                    <v-text-field v-model="finish"
                                  v-bind:rules="finish_rules"
                                  required
                                  label="Finish Time" name="finish" type="time" />
                    <v-select v-model="activity_id"
                              v-bind:items="activities"
                              v-bind:rules="activity_id_rules"
                              item-text="name"
                              item-value="activity_id"
                              label="Activity" name="activity"
                              required />
                </v-form>
            </v-card-text>
            <v-card-actions class="justify-center">
                <v-btn color="error"  :loading="deleting" v-on:click="delete_entry()" class="flex-grow-1">Delete</v-btn>
                <v-btn color="success" :loading="loading" v-on:click="submit()" class="flex-grow-1" v-bind:disabled="! valid">Save</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
export default {
    name: 'EditEmployeeTimesheetEntryForm',
    props: ['entry', 'dialog'],
    watch: {
        entry (new_entry) {
            if (new_entry) {
                this.initialize();
            }
        }
    },
    computed: {
        activities() {
            return this.$store.getters['activities/activities'];
        },
        _dialog: {
            get: function () {
                return this.dialog;
            },
            set: function (val) {
                this.$emit('update-dialog', val);
            }
        },
    },
    created () {
        this.$store.dispatch('activities/get_activities');
        this.initialize();
    },
    methods: {
        initialize() {
            if (this.entry) {
                this.employee_id = this.entry.employee_id;
                this.date = this.entry.date;

                this.start = this.entry.start;
                this.finish = this.entry.finish;

                this.activity_id = this.entry.activity_id;
            }
        },
        cancel() {
            this.close();
            this.reset();
        },
        delete_entry () {
            this.deleting = true;
            this.$store.dispatch('employees/delete_employee_timesheet_entry', this.entry)
                .then(() => {
                    this.deleting = false;
                    this.close();
                    this.reset();
                });
        },
        submit () {
            if (this.$refs.form.validate()) {
                this.loading = true;
                this.$store.dispatch('employees/put_employee_timesheet_entry', {
                    employee_id: this.employee_id,
                    date: this.date,
                    start: this.start,
                    finish: this.finish,
                    activity_id: this.activity_id,
                }).then(() => {
                    this.loading = false;
                    this.reset();
                    this.close();
                });
            }
        },
        close () {
            this.$emit('update-dialog', false);
        },
        reset () {
            this.employee_id = this.entry.employee_id;
            this.date = this.entry.date;
            this.start = this.entry.start;
            this.finish = this.entry.finish;
            this.activity_id = this.entry.activity_id;

            this.$refs.form.reset();
            this.$refs.form.resetValidation();
        },
    },
    data: function () {
        return {
            loading: false,
            deleting: false,
            title: 'Edit Entry',
            valid: false,
            errors: [],

            date: null,
            start: null,
            finish: null,
            activity_id: null,

            date_rules: [
                date => !!date || 'A Date is required',
            ],
            start_rules: [
                start => !!start || 'A Start Time is required',
            ],
            finish_rules: [
                finish => !!finish || 'A Finish Time is required',
            ],
            activity_id_rules: [
                activity_id => !!activity_id || 'An Activity is required',
            ],
        };
    },
};
</script>