<!--
This component is used to render a list of Activities currently in the application.
-->
<template>
    <v-list two-line class="py-0">

        <template v-for="(item, index) in activities">
            <v-list-item v-bind:key="item.activity_id"
                         exact
                         :to="{ name: 'activity', params: { activity_id: item.activity_id}}">
                <v-list-item-avatar>
                    <v-avatar :color="item.color ? item.color : 'indigo'" size="36">
                        <span class="white--text">{{ item.initials ? item.initials : 'ZZ'}}</span>
                    </v-avatar>
                </v-list-item-avatar>
                <v-list-item-content>
                    <v-list-item-title v-html="item.name"></v-list-item-title>
                    <v-list-item-subtitle v-html="item.code"></v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>
            <v-divider v-bind:key="index" />
        </template>

    </v-list>
</template>

<script>
/* eslint-disable */
export default {
    name: 'ActivitiesList',
    computed: {
        activities () {
            return this.$store.getters['activities/activities'];
        },
    },
    created() {
        this.initialize();
    },
    methods: {
        initialize() {
            this.loading = true;
            this.$store.dispatch('activities/get_activities')
                .then(() => {
                    this.loading = false;
                })
        },
    },
    data: function () {
        return {
            loading: false,
            loading_text: 'Loading Activities... please wait',
        };
    }
}
</script>
