<script lang="ts">
    import Table from "./Table.svelte";
    import client from "./lib/MQTT_Handler.svelte";
</script>

<h1>Restaurant</h1>

<div>
    <Table />
    <Table />
    <div class="flex-break"></div>
    <Table />
    <Table />
</div>

<style>
    h1 {
        text-align: center;
        font-size: 3.5rem;
        font-family: Arial, Helvetica, sans-serif;
    }

    div {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        row-gap: 100px;
        margin-top: 200px;
    }

    .flex-break {
        flex-basis: 100%;
        height: 0px;
    }
</style>
