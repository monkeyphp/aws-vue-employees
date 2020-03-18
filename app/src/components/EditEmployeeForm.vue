<!--
@file app/src/components/EditEmployeeForm.vue

This component is used to update an Employee.
-->
<template>
    <v-dialog v-model="_dialog" fullscreen hide-overlay transition="dialog-bottom-transition">
        <v-card v-bind:loading="loading" class="d-flex flex-column">

            <v-toolbar dark color="indigo" class="flex-grow-0">
                <v-btn icon dark v-on:click="cancel()"><v-icon>mdi-close</v-icon></v-btn>
                <v-toolbar-title>{{ title }}</v-toolbar-title>
            </v-toolbar>

            <v-card-text class="flex-grow-1 pt-5">
                <v-form v-model="valid" ref="form">
                    <v-text-field v-model="name"
                                  v-bind:rules="name_rules"
                                  v-bind:counter="name_counter"
                                  required
                                  label="Name" name="name" type="text" />
                    <v-text-field v-model="employee_id"
                                  readonly
                                  label="Employee Id" name="employee_id" type="text" />
                    <v-select v-model="parent_group_id"
                              v-bind:items="groups"
                              item-text="name"
                              item-value="group_id"
                              label="Group" name="parent_group_id"/>
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
/* eslint-disable */
export default {
    name: 'EditEmployeeForm',
    props: ['employee', 'dialog'],
    watch: {
        employee (new_employee) {
            if (new_employee) {
                this.initialize();
            }
        }
    },
    data: function () {
        return {
            loading: false,
            title: 'Edit Employee',
            valid: false,

            name: null,
            name_counter: 25,
            name_rules: [
                name => !!name || "A name is required",
            ],

            employee_id: null,
            parent_group_id: null,

        };
    },
    computed: {
        groups () {
            return this.$store.getters['groups/groups'];
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
    methods: {
        initialize() {
            const name = this.employee.name;
            this.name = name;
            this.title = `Edit ${name}`;
            this.employee_id = this.employee.employee_id;
            this.parent_group_id = this.employee.parent_group_id;

            this.loading = true;
            this.$store.dispatch('groups/get_groups')
                .finally(() => {
                    this.loading = false;
            });
        },
        cancel() {
            this.close();
            this.reset();
        },
        submit() {
            if (this.$refs.form.validate()) {
                this.loading = true;
                this.$store.dispatch('employees/put_employee', {
                    employee_id: this.employee_id,
                    name: this.name,
                    parent_group_id: this.parent_group_id,
                }).finally(() => {
                    this.loading = false;
                    this.close();
                    this.reset();
                });
            }
        },
        reset() {
            this.$refs.form.resetValidation();

            this.name = this.employee.name;
            this.employee_id = this.employee.employee_id;
            this.parent_group_id = this.employee.parent_group_id;
        },

        close() {
            this.$emit('update-dialog', false);
        },
    },
};
</script>