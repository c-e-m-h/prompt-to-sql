import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from 'recharts';

// data: [{ state: string, unique_customers: number }]
export default function Chart({ data }: { data: { state: string; unique_customers: number }[] }) {
  if (!data || data.length === 0) return <div>No chart data</div>;

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="state" />
        <YAxis allowDecimals={false} />
        <Tooltip />
        <Legend />
        <Bar dataKey="unique_customers" fill="#8884d8" name="Unique Customers" />
      </BarChart>
    </ResponsiveContainer>
  );
} 