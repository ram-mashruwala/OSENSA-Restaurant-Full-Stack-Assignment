<script lang="ts">
	let ordered: boolean = $state(false);
	import { connection_state } from "./lib/MQTT_Handler.svelte";
</script>

<div>
	{#if !ordered && connection_state.connected}
		<button onclick={() => (ordered = true)}>Order</button>
	{:else if !ordered && !connection_state.connected}
		<button disabled onclick={() => (ordered = true)}>Order</button>
	{:else}
		<p>Ordered! Your food is on the way!</p>
	{/if}
</div>

<style>
	div {
		width: 10em;
		height: 10em;
		border-radius: 50%;
		background-color: rgb(110, 57, 0);
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	button:hover {
		cursor: pointer;
	}
</style>
