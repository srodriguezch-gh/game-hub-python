/**
 * silrod-chart.js — Shared Chart.js configuration for silrod suite
 * Replaces per-app Chart.js configs with a standardized setup.
 */
(function() {
    'use strict';

    // Default chart configuration
    const SILROD_CHART_DEFAULTS = {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
            duration: 400,
            easing: 'easeOutQuart'
        },
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    font: {
                        family: "'Inter', sans-serif",
                        size: 11
                    },
                    padding: 16,
                    usePointStyle: true
                }
            },
            tooltip: {
                backgroundColor: 'rgba(30, 41, 59, 0.95)',
                titleFont: {
                    family: "'Inter', sans-serif",
                    size: 12,
                    weight: '600'
                },
                bodyFont: {
                    family: "'Inter', sans-serif",
                    size: 11
                },
                padding: 12,
                cornerRadius: 8,
                displayColors: true,
                usePointStyle: true
            }
        },
        scales: {
            x: {
                grid: {
                    display: false
                },
                ticks: {
                    font: {
                        family: "'Inter', sans-serif",
                        size: 10
                    }
                }
            },
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(0, 0, 0, 0.06)'
                },
                ticks: {
                    font: {
                        family: "'Inter', sans-serif",
                        size: 10
                    }
                }
            }
        }
    };

    // Color palette for charts
    const SILROD_CHART_COLORS = [
        { bg: 'rgba(59, 130, 246, 0.8)', border: '#3b82f6' },   // blue
        { bg: 'rgba(16, 185, 129, 0.8)', border: '#10b981' },   // emerald
        { bg: 'rgba(245, 158, 11, 0.8)', border: '#f59e0b' },   // amber
        { bg: 'rgba(239, 68, 68, 0.8)', border: '#ef4444' },    // red
        { bg: 'rgba(139, 92, 246, 0.8)', border: '#8b5cf6' },   // violet
        { bg: 'rgba(236, 72, 153, 0.8)', border: '#ec4899' },   // pink
        { bg: 'rgba(20, 184, 166, 0.8)', border: '#14b8a6' },   // teal
        { bg: 'rgba(251, 146, 60, 0.8)', border: '#fb923c' },   // orange
    ];

    // Apply defaults globally
    if (typeof Chart !== 'undefined') {
        Chart.defaults = Object.assign(Chart.defaults, SILROD_CHART_DEFAULTS);
        window.SILROD_CHART_COLORS = SILROD_CHART_COLORS;
    }

    // Export for use
    window.silrodCharts = {
        defaults: SILROD_CHART_DEFAULTS,
        colors: SILROD_CHART_COLORS,
        getColor: function(index) {
            return SILROD_CHART_COLORS[index % SILROD_CHART_COLORS.length];
        }
    };
})();