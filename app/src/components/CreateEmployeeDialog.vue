<!--
@file app/src/components/CreateEmployeeDialog.vue

This component is used to render a dialog (used in Admin view)
so that the user can add an Employee.
-->
<template>
    <v-dialog v-model="_dialog" fullscreen hide-overlay transition="dialog-bottom-transition">
        <v-card v-bind:loading="loading" class="d-flex flex-column">

            <v-toolbar dark color="indigo" class="flex-grow-0">
                <v-btn icon dark v-on:click="cancel()"><v-icon>mdi-close</v-icon></v-btn>
                <v-toolbar-title>{{ title }}</v-toolbar-title>
            </v-toolbar>

            <v-card-text class="flex-grow-1 pt-5">

                <v-alert dense type="error" transition="scale-transition" v-bind:value="error">
                    {{ message }}
                </v-alert>

                <v-form v-model="valid" ref="form">
                    <v-text-field v-model="name"
                                  v-bind:rules="name_rules"
                                  required
                                  v-bind:counter="name_counter"
                                  hint="The Employees name"
                                  label="Name" name="name" type="text" />
                    <v-select v-model="group_id"
                              v-bind:items="groups"
                              hint="The Employees Group"
                              item-text="name"
                              item-value="group_id"
                              label="Group" name="group_id" />
                    <v-text-field v-model="employee_id"
                                  v-bind:rules="employee_id_rules"
                                  required
                                  v-bind:counter="employee_id_counter"
                                  hint="The Employees id"
                                  label="Employee Id" name="employee_id" type="text" />
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
    name: 'CreateEmployeeDialog',
    props: ['dialog'],
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
    created () {
        this.initialize();
    },
    methods: {
        initialize() {
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
                const employee_id = this.employee_id;

                this.$store.dispatch('employees/post_employee', {
                    employee_id: employee_id,
                    name: this.name,
                    group_id: this.group_id,
                }).then(() => {
                    this.loading = false;
                    this.close();
                    this.reset();
                    this.$router.push({name: 'employee', params: {employee_id: employee_id}});

                }).catch((error) => {
                    // console.log(error);
                    // console.log(error.response);
                    // console.log(error.response.data);
                    // console.log(error.response.data.message);
                    // console.log(error.response.status);
                    // console.log(error.response.headers);
                    this.loading = false;

                    const message = error.response.data.error;
                    this.error = true;
                    this.message = message;
                });
            }
        },
        reset() {
            this.$refs.form.resetValidation();
            this.$refs.form.reset();

            this.error = false;
            this.message = null;

            this.initialize();
        },
        close() {
            this.$emit('update-dialog', false);
        },

    },
    data: function () {
        return {
            loading: false,
            title: 'Create Employee',

            valid: false,

            error: null,
            message: null,

            name: null,
            name_counter: 25,
            name_rules: [
                name => !!name || "A name is required",
            ],

            employee_id: null,
            employee_id_counter: 25,
            employee_id_rules: [
                employee_id => !!employee_id || "An employee id is required",
            ],

            group_id: null,
        };
    }
};
</script>
