type TableRow = {
  ordered: boolean
  arrived: boolean
  orderName: string
}

export const tableState = $state<TableRow[]>([])
