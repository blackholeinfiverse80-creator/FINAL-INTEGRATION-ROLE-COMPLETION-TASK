#!/usr/bin/env python3
"""
Generate Architecture Diagram PNG from existing markdown diagrams
Creates visual representation for final deliverable
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_architecture_diagram():
    """Create visual architecture diagram"""
    
    # Create figure and axis
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Colors
    colors = {
        'user': '#E3F2FD',
        'gateway': '#BBDEFB', 
        'business': '#90CAF9',
        'ai': '#64B5F6',
        'data': '#42A5F5'
    }
    
    # Title
    ax.text(8, 11.5, 'Core Integrator Architecture', 
            fontsize=20, fontweight='bold', ha='center')
    
    # Layer 1: User/Presentation
    user_box = FancyBboxPatch((1, 10), 14, 1, 
                              boxstyle="round,pad=0.1", 
                              facecolor=colors['user'], 
                              edgecolor='black', linewidth=2)
    ax.add_patch(user_box)
    ax.text(8, 10.5, 'USER (External Entity)\nHTTP/HTTPS Requests', 
            fontsize=12, ha='center', va='center', fontweight='bold')
    
    # Layer 2: API Gateway
    gateway_box = FancyBboxPatch((1, 8.5), 14, 1, 
                                 boxstyle="round,pad=0.1",
                                 facecolor=colors['gateway'], 
                                 edgecolor='black', linewidth=2)
    ax.add_patch(gateway_box)
    ax.text(8, 9, 'API GATEWAY LAYER\nRouting • Security (SSPL) • Authentication', 
            fontsize=12, ha='center', va='center', fontweight='bold')
    
    # Layer 3: Business Logic
    # Creator Router
    creator_box = FancyBboxPatch((1, 6.5), 4, 1.5, 
                                 boxstyle="round,pad=0.1",
                                 facecolor=colors['business'], 
                                 edgecolor='black', linewidth=1)
    ax.add_patch(creator_box)
    ax.text(3, 7.25, 'Creator Router\n• Context Prep\n• Module Route', 
            fontsize=10, ha='center', va='center')
    
    # Noopur Client
    noopur_client_box = FancyBboxPatch((6, 6.5), 4, 1.5, 
                                       boxstyle="round,pad=0.1",
                                       facecolor=colors['business'], 
                                       edgecolor='black', linewidth=1)
    ax.add_patch(noopur_client_box)
    ax.text(8, 7.25, 'Noopur Client\n• HTTP Client\n• Auth Headers', 
            fontsize=10, ha='center', va='center')
    
    # Enhancement
    enhance_box = FancyBboxPatch((11, 6.5), 4, 1.5, 
                                 boxstyle="round,pad=0.1",
                                 facecolor=colors['business'], 
                                 edgecolor='black', linewidth=1)
    ax.add_patch(enhance_box)
    ax.text(13, 7.25, 'Enhancement\n• Context Merge\n• Data Fusion', 
            fontsize=10, ha='center', va='center')
    
    # Layer 4: AI Processing
    # Noopur Backend
    noopur_backend_box = FancyBboxPatch((1, 4.5), 5, 1.5, 
                                        boxstyle="round,pad=0.1",
                                        facecolor=colors['ai'], 
                                        edgecolor='black', linewidth=1)
    ax.add_patch(noopur_backend_box)
    ax.text(3.5, 5.25, 'Noopur Backend\n• Flask App\n• AI Endpoints', 
            fontsize=10, ha='center', va='center')
    
    # AI Similarity
    similarity_box = FancyBboxPatch((6.5, 4.5), 4, 1.5, 
                                    boxstyle="round,pad=0.1",
                                    facecolor=colors['ai'], 
                                    edgecolor='black', linewidth=1)
    ax.add_patch(similarity_box)
    ax.text(8.5, 5.25, 'AI Similarity\n• Cosine Distance\n• Score Ranking', 
            fontsize=10, ha='center', va='center')
    
    # ML Pipeline
    ml_box = FancyBboxPatch((11, 4.5), 4, 1.5, 
                            boxstyle="round,pad=0.1",
                            facecolor=colors['ai'], 
                            edgecolor='black', linewidth=1)
    ax.add_patch(ml_box)
    ax.text(13, 5.25, 'ML Pipeline\n• Transformers\n• Embeddings', 
            fontsize=10, ha='center', va='center')
    
    # Layer 5: Data Persistence
    # Noopur SQLite
    noopur_db_box = FancyBboxPatch((1, 2.5), 4.5, 1.5, 
                                   boxstyle="round,pad=0.1",
                                   facecolor=colors['data'], 
                                   edgecolor='black', linewidth=1)
    ax.add_patch(noopur_db_box)
    ax.text(3.25, 3.25, 'Noopur SQLite\n• AI Embeddings\n• Generated Content', 
            fontsize=10, ha='center', va='center')
    
    # Core Integrator DB
    core_db_box = FancyBboxPatch((6, 2.5), 4, 1.5, 
                                 boxstyle="round,pad=0.1",
                                 facecolor=colors['data'], 
                                 edgecolor='black', linewidth=1)
    ax.add_patch(core_db_box)
    ax.text(8, 3.25, 'Core Integrator DB\n• User Context\n• Interactions', 
            fontsize=10, ha='center', va='center')
    
    # MongoDB Atlas
    mongo_box = FancyBboxPatch((10.5, 2.5), 4.5, 1.5, 
                               boxstyle="round,pad=0.1",
                               facecolor=colors['data'], 
                               edgecolor='black', linewidth=1)
    ax.add_patch(mongo_box)
    ax.text(12.75, 3.25, 'MongoDB Atlas\n• Cloud Storage\n• Scalability', 
            fontsize=10, ha='center', va='center')
    
    # AI Model Components Box
    ai_model_box = FancyBboxPatch((2, 0.5), 12, 1.5, 
                                  boxstyle="round,pad=0.1",
                                  facecolor='#FFF3E0', 
                                  edgecolor='orange', linewidth=2)
    ax.add_patch(ai_model_box)
    ax.text(8, 1.25, 'AI MODEL COMPONENTS\nSentence Transformers (all-MiniLM-L6-v2) • NumPy • SciPy • Embeddings', 
            fontsize=11, ha='center', va='center', fontweight='bold')
    
    # Add arrows for data flow
    # User to Gateway
    ax.arrow(8, 10, 0, -0.4, head_width=0.2, head_length=0.1, fc='black', ec='black')
    
    # Gateway to Business Logic
    ax.arrow(8, 8.5, 0, -0.4, head_width=0.2, head_length=0.1, fc='black', ec='black')
    
    # Business Logic connections
    ax.arrow(5, 7.25, 0.8, 0, head_width=0.1, head_length=0.1, fc='blue', ec='blue')
    ax.arrow(10, 7.25, 0.8, 0, head_width=0.1, head_length=0.1, fc='blue', ec='blue')
    
    # Business to AI
    ax.arrow(8, 6.5, 0, -0.4, head_width=0.2, head_length=0.1, fc='green', ec='green')
    
    # AI to Data
    ax.arrow(8.5, 4.5, 0, -0.4, head_width=0.2, head_length=0.1, fc='red', ec='red')
    
    # Add legend
    legend_elements = [
        patches.Patch(color=colors['user'], label='Presentation Layer'),
        patches.Patch(color=colors['gateway'], label='API Gateway Layer'),
        patches.Patch(color=colors['business'], label='Business Logic Layer'),
        patches.Patch(color=colors['ai'], label='AI Processing Layer'),
        patches.Patch(color=colors['data'], label='Data Persistence Layer')
    ]
    
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    # Add performance metrics
    ax.text(0.5, 0.2, 'Performance: <200ms response • 1000+ req/min • 99.9% uptime', 
            fontsize=10, style='italic')
    
    plt.tight_layout()
    return fig

def create_data_flow_diagram():
    """Create data flow diagram"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'Level 1 Data Flow Diagram', 
            fontsize=18, fontweight='bold', ha='center')
    
    # External Entity - User
    user_circle = plt.Circle((2, 8), 0.8, color='lightblue', ec='black', linewidth=2)
    ax.add_patch(user_circle)
    ax.text(2, 8, 'USER', fontsize=10, ha='center', va='center', fontweight='bold')
    
    # Processes
    processes = [
        (4, 8, 'P1:\nGateway'),
        (6.5, 8, 'P2:\nCreator\nRouter'),
        (9, 8, 'P3:\nNoopur\nClient'),
        (11.5, 8, 'P4:\nNoopur\nBackend'),
        (11.5, 5.5, 'P5:\nAI\nSimilarity'),
        (9, 5.5, 'P6:\nEnhance\nment'),
        (6.5, 5.5, 'P7:\nMemory\nStorage'),
        (4, 5.5, 'P8:\nAgent\nResponse')
    ]
    
    for x, y, label in processes:
        process_box = FancyBboxPatch((x-0.6, y-0.6), 1.2, 1.2, 
                                     boxstyle="round,pad=0.1",
                                     facecolor='lightgreen', 
                                     edgecolor='black', linewidth=1)
        ax.add_patch(process_box)
        ax.text(x, y, label, fontsize=9, ha='center', va='center', fontweight='bold')
    
    # Data Stores
    datastores = [
        (2, 3, 'DS1:\nNoopur\nSQLite'),
        (7, 3, 'DS2:\nCore\nIntegrator'),
        (12, 3, 'DS3:\nMongoDB\nAtlas')
    ]
    
    for x, y, label in datastores:
        ds_box = FancyBboxPatch((x-0.8, y-0.6), 1.6, 1.2, 
                                boxstyle="round,pad=0.1",
                                facecolor='lightyellow', 
                                edgecolor='black', linewidth=1)
        ax.add_patch(ds_box)
        ax.text(x, y, label, fontsize=9, ha='center', va='center', fontweight='bold')
    
    # Data flows (arrows)
    flows = [
        # User to P1
        ((2.8, 8), (3.4, 8), 'Request'),
        # P1 to P2
        ((4.6, 8), (5.9, 8), 'Route'),
        # P2 to P3
        ((7.1, 8), (8.4, 8), 'Context'),
        # P3 to P4
        ((9.6, 8), (10.9, 8), 'HTTP'),
        # P4 to DS1
        ((11.5, 7.4), (2.8, 3.6), 'Query'),
        # DS1 to P5
        ((2.8, 3.6), (10.9, 5.5), 'Data'),
        # P5 to P6
        ((10.9, 5.5), (9.6, 5.5), 'Context'),
        # P6 to P7
        ((8.4, 5.5), (7.1, 5.5), 'Enhanced'),
        # P7 to DS2
        ((6.5, 4.9), (7, 3.6), 'Store'),
        # P7 to P8
        ((5.9, 5.5), (4.6, 5.5), 'Data'),
        # P8 to User
        ((3.4, 5.5), (2.8, 7.2), 'Response')
    ]
    
    for (start, end, label) in flows:
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='blue'))
        # Add label at midpoint
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        ax.text(mid_x, mid_y + 0.2, label, fontsize=8, ha='center', 
                bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    return fig

def main():
    """Generate architecture diagrams"""
    print("Generating Architecture Diagrams...")
    
    # Create architecture diagram
    arch_fig = create_architecture_diagram()
    arch_fig.savefig('architecture_diagram.png', dpi=300, bbox_inches='tight')
    print("Architecture diagram saved: architecture_diagram.png")
    
    # Create data flow diagram
    dfd_fig = create_data_flow_diagram()
    dfd_fig.savefig('data_flow_diagram.png', dpi=300, bbox_inches='tight')
    print("Data flow diagram saved: data_flow_diagram.png")
    
    plt.close('all')
    print("\nArchitecture diagrams generated successfully!")

if __name__ == "__main__":
    main()