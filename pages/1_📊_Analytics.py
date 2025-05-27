import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import os
from vector_store.chroma_store import collection
from collections import Counter
import re

st.set_page_config(
    page_title="Analytics - IntelliDoc",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .analytics-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def get_collection_stats():
    """Get statistics from the vector store collection"""
    try:
        # Get all documents
        results = collection.get()
        
        if not results['documents']:
            return None
        
        documents = results['documents']
        ids = results['ids']
        
        # Calculate statistics
        total_docs = len(documents)
        total_chars = sum(len(doc) for doc in documents)
        avg_doc_length = total_chars / total_docs if total_docs > 0 else 0
        
        # Word frequency analysis
        all_text = ' '.join(documents)
        words = re.findall(r'\b\w+\b', all_text.lower())
        word_freq = Counter(words)
        
        # Document length distribution
        doc_lengths = [len(doc) for doc in documents]
        
        return {
            'total_docs': total_docs,
            'total_chars': total_chars,
            'avg_doc_length': avg_doc_length,
            'word_freq': word_freq,
            'doc_lengths': doc_lengths,
            'documents': documents,
            'ids': ids
        }
    except Exception as e:
        st.error(f"Error getting collection stats: {str(e)}")
        return None

def create_word_cloud_data(word_freq, top_n=20):
    """Create data for word frequency visualization"""
    # Filter out common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
    
    filtered_freq = {word: count for word, count in word_freq.items() 
                    if word not in stop_words and len(word) > 2}
    
    top_words = dict(sorted(filtered_freq.items(), key=lambda x: x[1], reverse=True)[:top_n])
    
    return top_words

def main():
    st.markdown('<h1 class="analytics-header">📊 Document Analytics</h1>', unsafe_allow_html=True)
    
    # Get collection statistics
    stats = get_collection_stats()
    
    if stats is None:
        st.info("📭 No documents found in the collection. Upload some documents to see analytics!")
        return
    
    # Key Metrics Row
    st.markdown("## 📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📚 Total Documents",
            value=stats['total_docs'],
            delta=None
        )
    
    with col2:
        st.metric(
            label="📝 Total Characters",
            value=f"{stats['total_chars']:,}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="📏 Avg Document Length",
            value=f"{stats['avg_doc_length']:.0f} chars",
            delta=None
        )
    
    with col4:
        st.metric(
            label="🔤 Unique Words",
            value=f"{len(stats['word_freq']):,}",
            delta=None
        )
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Document Length Distribution")
        
        # Create histogram of document lengths
        fig_hist = px.histogram(
            x=stats['doc_lengths'],
            nbins=20,
            title="Distribution of Document Lengths",
            labels={'x': 'Document Length (characters)', 'y': 'Number of Documents'},
            color_discrete_sequence=['#667eea']
        )
        fig_hist.update_layout(
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        st.markdown("### 🔤 Top Words Frequency")
        
        # Create word frequency chart
        top_words = create_word_cloud_data(stats['word_freq'], 15)
        
        if top_words:
            words_df = pd.DataFrame(list(top_words.items()), columns=['Word', 'Frequency'])
            
            fig_words = px.bar(
                words_df,
                x='Frequency',
                y='Word',
                orientation='h',
                title="Most Frequent Words",
                color='Frequency',
                color_continuous_scale='Viridis'
            )
            fig_words.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig_words, use_container_width=True)
    
    # Document Details Section
    st.markdown("## 📋 Document Details")
    
    # Create a dataframe for document details
    doc_data = []
    for i, (doc_id, doc_text) in enumerate(zip(stats['ids'], stats['documents'])):
        doc_data.append({
            'Document ID': doc_id[:8] + '...',  # Shortened ID for display
            'Length (chars)': len(doc_text),
            'Word Count': len(doc_text.split()),
            'Preview': doc_text[:100] + '...' if len(doc_text) > 100 else doc_text
        })
    
    docs_df = pd.DataFrame(doc_data)
    
    # Display the dataframe
    st.dataframe(
        docs_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Document ID": st.column_config.TextColumn("Document ID", width="small"),
            "Length (chars)": st.column_config.NumberColumn("Length (chars)", width="small"),
            "Word Count": st.column_config.NumberColumn("Word Count", width="small"),
            "Preview": st.column_config.TextColumn("Preview", width="large")
        }
    )
    
    # Advanced Analytics Section
    st.markdown("## 🔍 Advanced Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Document Size Analysis")
        
        # Box plot for document lengths
        fig_box = go.Figure()
        fig_box.add_trace(go.Box(
            y=stats['doc_lengths'],
            name="Document Lengths",
            boxpoints='outliers',
            marker_color='#667eea'
        ))
        fig_box.update_layout(
            title="Document Length Distribution (Box Plot)",
            yaxis_title="Characters",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Collection Summary")
        
        # Summary statistics
        doc_lengths = stats['doc_lengths']
        summary_stats = {
            'Minimum Length': min(doc_lengths),
            'Maximum Length': max(doc_lengths),
            'Median Length': sorted(doc_lengths)[len(doc_lengths)//2],
            'Standard Deviation': pd.Series(doc_lengths).std()
        }
        
        for stat, value in summary_stats.items():
            st.metric(stat, f"{value:.0f} chars")
    
    # Export Options
    st.markdown("## 📤 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Analytics Data"):
            # Create export data
            export_data = {
                'summary': {
                    'total_documents': stats['total_docs'],
                    'total_characters': stats['total_chars'],
                    'average_length': stats['avg_doc_length'],
                    'unique_words': len(stats['word_freq'])
                },
                'document_details': doc_data,
                'top_words': dict(list(create_word_cloud_data(stats['word_freq'], 50).items()))
            }
            
            st.download_button(
                label="💾 Download JSON",
                data=pd.Series(export_data).to_json(),
                file_name=f"intellidoc_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📋 Export Document List"):
            st.download_button(
                label="💾 Download CSV",
                data=docs_df.to_csv(index=False),
                file_name=f"document_list_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
