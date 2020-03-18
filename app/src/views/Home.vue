<!--
@file app/src/views/Home.vue

This component is used to render the (default) page.
-->
<template>
    <div>
        <v-app-bar app color="indigo" dark>
            <v-toolbar-title>
                {{ title }}
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn icon>
                <v-icon>mdi-magnify</v-icon>
            </v-btn>

            <v-menu left bottom>
                <template v-slot:activator="{ on }">
                    <v-btn icon v-on="on">
                        <v-icon>mdi-dots-vertical</v-icon>
                    </v-btn>
                </template>

                <v-list>
                    <v-list-item>
                        <v-list-item-title>Settings (home)</v-list-item-title>
                    </v-list-item>
                    <v-list-item>
                        <v-list-item-title>About (home)</v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>
        </v-app-bar>

        <v-content>
            <v-container>
                <Settings />
                <Version />
                <router-view />
            </v-container>
        </v-content>

    </div>
</template>

<script>
import Settings from '@/components/Settings.vue';
import Version from '@/components/Version.vue';

export default {
    name: 'Home',
    components: {
        Settings,
        Version
    },
    data: function () {
        return {
            title: 'TimeBox',
        }
    }
};
</script>