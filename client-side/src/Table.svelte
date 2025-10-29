<!-- 
@component

This is a Table component that represents a single table in a restaurant
ordering system. It uses the MQTT Handler to manage order states
and displays the current status of the table. Users can place an order,
view the order status, and clear the table once the order has arrived.

PROPS:

id: number
	This is the id of the table, which is used to place and recieve orders and manage 
	the state of the table

-->

<script lang="ts">
	import { connection_state, Order } from "./lib/MQTT_Handler.svelte";
	import { tableState } from "./lib/state.svelte";

	const { id } = $props();

	let ordered: boolean = $derived(tableState[id - 1]["ordered"]);
	let arrived: boolean = $derived(tableState[id - 1]["arrived"]);
</script>

<div>
	<p>{id}</p>
	{#if !connection_state.connected}
		<button disabled onclick={() => (ordered = true)}>Order</button>
	{:else if !ordered}
		<button
			onclick={() => {
				const orderTemp: string | null = window.prompt(
					"Please Enter in the name of the Food you want.",
				);
				if (orderTemp == null) {
					return;
				}
				Order(id, orderTemp);
			}}>Order</button
		>
	{:else if ordered && !arrived}
		<p>Ordered! Your food is on the way!</p>
	{:else if arrived}
		<p>{tableState[id - 1]["orderName"]}</p>
		<button
			onclick={() => {
				tableState[id - 1]["ordered"] = false;
				tableState[id - 1]["arrived"] = false;
			}}>Clear Table</button
		>
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

	p {
		color: white;
		text-align: center;
	}
</style>
