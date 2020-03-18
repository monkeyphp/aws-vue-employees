<!--
@file app/src/components/EditActivityDialog.vue

This component is used to render a form for editing an Activity.
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
                                  label="Name" name="name" type="text"></v-text-field>
                    <v-text-field v-model="code"
                                  v-bind:rules="code_rules"
                                  v-bind:counter="code_counter"
                                  label="Code" name="code" type="text"></v-text-field>
                    <v-text-field v-model="description"
                                  v-bind:rules="description_rules"
                                  v-bind:counter="description_counter"
                                  label="Description" name="description" type="text"></v-text-field>
                    <v-checkbox v-model="worked"
                                hint="This Activity is worked"
                                label="Worked" name="worked" type="checkbox"></v-checkbox>
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
    name: 'EditActivityDialog',
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
        initialize () {
            const name = this.activity.name;
            this.name = name;
            this.title = `Edit ${name}`;
            this.activity_id = this.activity.activity_id;
            this.code = this.activity.code;
            this.description = this.activity.description;
            this.worked = this.activity.worked;
        },
        cancel() {
            this.close();
            this.reset();
        },
        submit() {
            if (this.$refs.form.validate()) {
                this.loading = true;
                this.$store.dispatch('activities/put_activity', {
                    activity_id: this.activity_id,
                    name: this.name,
                    code: this.code,
                    description: this.description,
                    worked: this.worked,
                }).then(() => {
                    this.loading = false;
                    this.close();
                    this.reset();
                });
            }
        },
        reset() {
            this.$refs.form.resetValidation();
            this.initialize();
        },
        close() {
            this.$emit('update-dialog', false);
        }
    },
    data: function () {
        return {
            loading: false,
            title: 'Edit Activity',
            valid: false,

            name: null,
            name_counter: 25,
            name_rules: [
                name => !!name || "A name is required",
            ],

            code: null,
            code_counter: 25,
            code_rules: [

            ],

            description: null,
            description_counter: 50,
            description_rules: [

            ],

            worked: null,
        };
    },
};
</script>