import ReactFlow, { MiniMap, Controls, Background } from 'react-flow';

const flowchartElements = [
  { id: '1', type: 'input', data: { label: 'Course' }, position: { x: 50, y: 50 } },
  { id: '2', data: { label: 'Certification' }, position: { x: 200, y: 50 } },
  { id: '3', data: { label: 'Business Analyst' }, position: { x: 350, y: 50 } },
  { id: '4', data: { label: 'Zone Leader' }, position: { x: 500, y: 50 } },
  { id: '5', data: { label: 'Region Leader' }, position: { x: 650, y: 50 } },
  { id: '6', data: { label: 'State Leader' }, position: { x: 800, y: 50 } },
  { id: '7', type: 'output', data: { label: 'Country Leader' }, position: { x: 950, y: 50 } },
  // Define connections between nodes
  { id: 'e1-2', source: '1', target: '2', animated: true },
  { id: 'e2-3', source: '2', target: '3', animated: true },
  { id: 'e3-4', source: '3', target: '4', animated: true },
  { id: 'e4-5', source: '4', target: '5', animated: true },
  { id: 'e5-6', source: '5', target: '6', animated: true },
  { id: 'e6-7', source: '6', target: '7', animated: true },
];

const FlowChart = () => (

  <div style={{ height: 300, width: '100%', borderRadius: '8px', border: '1px solid #28a745' }}>
    <ReactFlow elements={flowchartElements}>
      <MiniMap />
      <Controls />
      <Background />
    </ReactFlow>
  </div>
);
export default FlowChart;
