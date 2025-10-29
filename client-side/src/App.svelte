<script lang="ts">
    import Table from "./Table.svelte";
    import client from "./lib/MQTT_Handler.svelte";
    import { connection_state } from "./lib/MQTT_Handler.svelte";

    import { tableState } from "./lib/state.svelte";

    const LENGTH: number = 6;

    for (let i: number = 0; i < LENGTH; i++) {
        tableState.push({ ordered: false, arrived: false, orderName: "" });
    }

    function* range(start: number, end: number): Generator<number> {
        for (let i = start; i < end; i++) yield i;
    }
</script>

<h1>Restaurant</h1>

{#if !connection_state.connected}
    <h2>Connecting to MQTT Server ...</h2>
{/if}
<div>
    {#each range(1, LENGTH + 1) as id}
        <Table {id} />
    {/each}
</div>

<style>
    h1 {
        text-align: center;
        font-size: 4vw;
        font-family: Arial, Helvetica, sans-serif;
    }

    h2 {
        text-align: center;
        font-size: 2vw;
        font-family: Arial, Helvetica, sans-serif;
        color: red;
    }

    div {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        row-gap: 15vh;
        margin-top: 20vh;
        column-gap: 30vw;
    }

    .flex-break {
        flex-basis: 100%;
        height: 0px;
    }
</style>
