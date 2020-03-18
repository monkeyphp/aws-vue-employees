<!--
@file app/src/components/CreateEmployeeTimesheetEntryForm.vue

This component is used to render a form for adding an Entry.
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
                <v-btn color="indigo" text  v-on:click="cancel()" class="flex-grow-1">Cancel</v-btn>
                <v-btn color="success" :loading="loading" v-on:click="submit()" class="flex-grow-1" v-bind:disabled="! valid">Save</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>
<script>
export default {
    name: 'CreateEmployeeTimesheetEntryForm',
    props: ['employee_id', 'dialog', 'timesheet_date'],
    watch: {
        employee_id (new_employee_id) {
            if (new_employee_id) {
                this.initialize();
            }
        },
    },
    computed: {
        employee () {
            let _employee = null;
            if (this.employee_id) {
                _employee = this.$store.getters['employees/employee'](this.employee_id);
            }
            return _employee;
        },
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
        initialize () {
            this.date = this.timesheet_date;
        },
        cancel () {
            this.close();
            this.reset();
        },
        submit () {
            if (this.$refs.form.validate()) {
                this.loading = true;
                this.$store.dispatch('employees/post_employee_timesheet_entry', {
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
            this.date = null;
            this.time = null;
            this.time = null;
            this.activity_id = null;
            this.$refs.form.reset();
            this.$refs.form.resetValidation();
        },
    },
    data: function () {
        return {
            loading: false,
            title: 'Create Entry',
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
}
</script>