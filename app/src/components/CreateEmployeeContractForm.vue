<!--
@file app/src/components/CreateEmployeeContractForm.vue

This component is used to render a dialog for creating a Contract for the specified Employee.
-->
<template>
    <v-dialog v-model="_dialog" fullscreen hide-overlay transition="dialog-bottom-transition">
        <v-card v-bind:loading="loading" class="d-flex flex-column">

            <v-toolbar dark color="indigo" class="flex-grow-0">
                <v-btn icon dark v-on:click="cancel()"><v-icon>mdi-close</v-icon></v-btn>
                <v-toolbar-title>{{ title }}</v-toolbar-title>
            </v-toolbar>

            <v-card-text class="flex-grow-1 pt-5">
                <v-form v-model="valid" ref="form" lazy-evaluation>
                    <v-text-field v-model="start_date"
                                  v-bind:rules="start_date_rules"
                                  required
                                  label="Start" name="start_date" type="date" />
                    <v-text-field v-model="weekly_hours"
                                  v-bind:rules="weekly_hours_rules"
                                  required
                                  label="Weekly Hours" name="weekly_hours" type="text"/>
                    <v-text-field v-model="hourly_rate"
                                  v-bind:rules="hourly_rate_rules"
                                  prefix="£"
                                  required
                                  label="Hourly Rate" name="hourly_rate" type="text" />
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
    name: 'CreateEmployeeContractForm',
    props: ['employee_id', 'dialog'],
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
        _dialog: {
            get: function () {
                return this.dialog;
            },
            set: function (val) {
                this.$emit('update-dialog', val);
            }
        },
    },
    data: function () {
        return {
            loading: false,
            title: 'Create Contract',

            valid: false,
            errors: [],

            start_date: null,
            weekly_hours: null,
            hourly_rate: null,

            start_date_rules: [
                start_date => !!start_date || 'A Start Date is required',
            ],
            weekly_hours_rules: [
                weekly_hours => !!weekly_hours || 'A Weekly Hours is required',
            ],
            hourly_rate_rules: [
                hourly_rate => !!hourly_rate || 'An Hourly Rate is required',
            ]
        };
    },
    created() {
        this.initialize();
    },
    methods: {
        initialize() {
            //
        },
        cancel() {
            this.close();
            this.reset();
        },
        submit() {
            if (this.$refs.form.validate()) {
                this.loading = true;
                this.$store.dispatch('employees/post_employee_contract', {
                    employee_id: this.employee_id,
                    start_date: this.start_date,
                    weekly_hours: this.weekly_hours,
                    hourly_rate: this.hourly_rate
                }).then(() => {
                    this.loading = false;
                    this.close();
                    this.reset();
                });
            }
        },
        reset() {
            this.start_date = null;
            this.weekly_hours = null;
            this.hourly_rate = null;

            this.$refs.form.reset();
            this.$refs.form.resetValidation();
        },
        close() {
            this.$emit('update-dialog', false);
        },
    }
}
</script>