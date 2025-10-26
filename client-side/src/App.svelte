<script lang="ts">
	import Table from "./Table.svelte";
</script>

<main>
	<h1>Restaurant Simulation</h1>
	<div>
		<Table />
		<Table />
		<div class="flex-break" />
		<Table />
		<Table />
	</div>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		font-size: 4em;
		font-weight: 100;
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

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
