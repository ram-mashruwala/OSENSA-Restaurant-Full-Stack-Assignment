type TableRow = {
  ordered: boolean
  arrived: boolean
  orderName: string
}

export const tableState = $state<TableRow[]>([
  { ordered: false, arrived: false, orderName: "" },
  { ordered: false, arrived: false, orderName: "" },
  { ordered: false, arrived: false, orderName: "" },
  { ordered: false, arrived: false, orderName: "" },
])
