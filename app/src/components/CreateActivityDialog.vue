<!--
@file app/src/components/CreateActivityDialog.vue

This component is used to create a new Activity and post it to the store.
-->
<template>
    <v-dialog v-model="_dialog" fullscreen hide-overlay transition="dialog-bottom-transition">

        <v-card v-bind:loading="loading" class="d-flex flex-column" tile>
            <v-toolbar dark color="indigo" class="flex-grow-0">
                <v-btn icon dark @click="_dialog = false"><v-icon>mdi-close</v-icon></v-btn>
                <v-toolbar-title>{{ title }}</v-toolbar-title>
            </v-toolbar>
            <v-card-text class="flex-grow-1 pt-5">
                <v-form v-model="valid" ref="form" lazy-evaluation>
                    <v-text-field v-model="name"
                                  v-bind:rules="name_rules"
                                  v-bind:counter="name_counter"
                                  hint="The name of the Activity"
                                  required
                                  label="Name" name="name" type="text" />
                    <v-text-field v-model="code"
                                  v-bind:rules="code_rules"
                                  v-bind:counter="code_counter"
                                  hint="The code of the Activity"
                                  label="Code" name="code" type="text" />
                    <v-text-field v-model="description"
                                  v-bind:rules="description_rules"
                                  v-bind:counter="description_counter"
                                  hint="The description of the Activity"
                                  label="Description" name="description" type="text" />
                    <v-checkbox v-model="worked"
                                hint="This Activity is worked"
                                label="Worked" name="worked" type="checkbox" />
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
    name: 'CreateActivityDialog',
    props: ['dialog'],
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
    data: function () {
        return {
            loading: false,
            title: 'Create Activity',
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
            worked: false,
        }
    },
    created () {
        this.initialize();
    },
    methods: {
        initialize () {
            //
        },
        cancel() {
            this.close();
            this.reset();
        },
        submit() {
            if (this.$refs.form.validate()) {
                this.loading = true;
                this.$store.dispatch('activities/post_activity', {
                    name: this.name,
                    code: this.code,
                    description: this.description,
                    worked: this.worked
                }).then((activity) => {
                    this.loading = false;
                    this.close();
                    this.reset();

                    const activity_id = activity.activity_id;
                    this.$router.push({name: 'activity', params: {activity_id: activity_id}});
                });
            }
        },
        reset() {
            this.$refs.form.resetValidation();
            this.$refs.form.reset();
            this.initialize()
        },
        close () {
            this.$emit('update-dialog', false);
        },
    }
}
</script>